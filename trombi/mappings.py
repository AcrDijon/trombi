# encoding: utf8
import os
import unicodedata
import re

from passlib.utils import generate_password
from passlib.hash import sha256_crypt
from mailer import Mailer, Message

from sqlalchemy_utils import EmailType, PasswordType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Column, Integer, Unicode, Enum, ForeignKey, Date,
                        Boolean, ForeignKeyConstraint, String, Float,
                        UnicodeText)
from sqlalchemy.orm import column_property, relationship


Base = declarative_base()


class Hash(Base):
    __tablename__ = 'hash'

    name = Column(Unicode(128), primary_key=True)
    value = Column(String(256))

    def __init__(self, name=None, value=None):
        if name:
            self.name = name
        if value:
            self.value = value


class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    label = Column(Unicode(128))
    zipcode = Column(Integer)

    def __init__(self, label=None, zipcode=None):
        if label:
            self.label = label
        if zipcode:
            self.zipcode = zipcode

    def __eq__(self, other):
        if other is None:
            return False
        return self.label == other.label and self.zipcode == other.zipcode

    def __str__(self):
        return '%s (%s)' % (self.label, self.zipcode)


class Category(Base):
    __tablename__ = 'category'

    code = Column(String(2), primary_key=True)
    label = Column(Unicode(128))
    min_age = Column(Integer)
    max_age = Column(Integer)

    def __eq__(self, other):
        if other is None:
            return False
        return self.code == other.code


class Membership(Base):
    __tablename__ = 'membership'

    label = Column(Unicode(128), primary_key=True)
    price = Column(Float(asdecimal=True))

    def __eq__(self, other):
        return self.label == other.label

_BODY = u"""\
Bonjour,

Vous avez demandé une ré-initialization de votre mot de passe.

Veuillez suivre ce lien:

    http://trombi.acr-dijon.org/change_password?token=%s&login=%s

Si vous n'avez jamais fait cette demande, vous pouvez ignorer cet email.

--
L'équipe ACR Dijon
"""


class Member(Base):
    __tablename__ = 'member'

    id = Column(Integer, primary_key=True)
    membership_label = Column(Unicode(128), ForeignKey('membership.label'))
    membership = relationship(Membership)
    category_code = Column(String(2), ForeignKey('category.code'))
    category = relationship(Category)
    permissions = Column(Enum("User", "Admin", "Owner"))
    lastname = Column(Unicode(128))
    firstname = Column(Unicode(128))
    login = Column(Unicode(128))
    password = Column(PasswordType(schemes=['sha256_crypt']))
    email = Column(EmailType)
    licence = Column(Unicode(128))
    gender = Column(Enum('M', 'F'))
    address = Column(Unicode(256))
    city_id = Column(Integer, ForeignKey('city.id'))
    city = relationship(City)
    phone = Column(String(10))
    phone2 = Column(String(10))
    birthday = Column(Date)
    medical_certificate_date = Column(Date)
    is_published = Column(Boolean)
    has_paid = Column(Boolean)
    last_updated = Column(Date)
    bio = Column(UnicodeText)
    token = Column(String(64))

    def normalize(self, value):
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
        value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
        return unicode(re.sub('[-\s]+', '', value))

    @property
    def is_super_user(self):
        return (self.permissions == u'Admin' or
                self.permissions == u'Owner')


    def set_login(self):
        login = '%s%s' % (self.firstname.lower(),
                          self.lastname.lower())

        self.login = self.normalize(login)

    def set_password(self, password=None):
        if password is None:
            password = generate_password()
        self.password = password

    def verify_password(self, password):
        hashed = member.password.hash
        return sha256_crypt.verify(password, hashed)

    def send_reset_email(self):
        self.token = os.urandom(32).encode('hex')
        sender = Mailer('localhost', port=25)
        msg = Message(From="tarek@ziade.org", To=[self.email],
                      charset="utf-8")
        msg.Subject = u'Accès trombinoscope ACR'
        msg.Body = _BODY % (unicode(self.token), unicode(self.login))
        sender.send([msg])


Member.__table__.sqlite_autoincrement = True


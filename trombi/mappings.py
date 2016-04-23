from sqlalchemy_utils import EmailType, PasswordType

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Column, Integer, Unicode, Enum, ForeignKey, Date,
                        Boolean, ForeignKeyConstraint, String, Float)
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
        return self.label == other.label and self.zipcode == other.zipcode



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
    password = Column(PasswordType(schemes=['pbkdf2_sha512']))
    email = Column(EmailType)
    licence = Column(Unicode(128))
    gender = Column(Enum('M', 'F'))
    address = Column(Unicode(256))
    city_id = Column(Integer, ForeignKey('city.id'))
    city = relationship(City)
    phone = Column(String(10))
    birthday = Column(Date)
    medical_certificate_date = Column(Date)
    is_published = Column(Boolean)
    has_paid = Column(Boolean)
    last_updated = Column(Date)


Member.__table__.sqlite_autoincrement = True


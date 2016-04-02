from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Column, Integer, Unicode, Enum, ForeignKey, Date,
                        Boolean, ForeignKeyConstraint, String)
from sqlalchemy.orm import column_property


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
    label = Column(Unicode(128), primary_key=True)
    zipcode = Column(Integer, primary_key=True)

    def __init__(self, label=None, zipcode=None):
        if label:
            self.label = label
        if zipcode:
            self.zipcode = zipcode


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    label = Column(Unicode(128))
    min_age = Column(Integer)
    max_age = Column(Integer)


class Membership(Base):
    __tablename__ = 'membership'

    id = Column(Integer, primary_key=True)
    label = Column(Unicode(128))
    price = Column(Integer)


class Member(Base):
    __tablename__ = 'member'

    id = Column(Integer, primary_key=True)
    membership = Column(Integer, ForeignKey('membership.id'))
    category = Column(Integer, ForeignKey('category.id'))
    permissions = Column(Enum("User", "Admin", "Owner"))
    picture = Column(Unicode(128))
    lastname = Column(Unicode(128))
    firstname = Column(Unicode(128))
    password = Column(Unicode(128))
    email = Column(Unicode(128))
    licence = Column(Unicode(128))
    gender = Column(Enum('M', 'F'))
    address = Column(Unicode(256))

    city_label = Column(Unicode(128))
    city_zipcode = Column(Integer)
    ForeignKeyConstraint(['city_label', 'city_zipcode'], ['city.label', 'city.zipcode'])

    phone = Column(Integer)
    birthday = Column(Date)
    medical_certificate_date = Column(Date)
    is_published = Column(Boolean)
    has_paid = Column(Boolean)
    last_updated = Column(Date)

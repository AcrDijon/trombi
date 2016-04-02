import datetime
import csv
import os
import hashlib

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from trombi import mappings


Session = sessionmaker()


def get_hash(session, name):
    res = session.query(mappings.Hash).filter_by(name=name).first()
    if res is None:
        return None
    return res.value


def set_hash(session, name, value):
    hash = session.query(mappings.Hash).filter_by(name=name).first()
    if hash is None:
        hash = mappings.Hash(name, value)
    else:
        hash.value = value

    session.add(hash)
    session.commit()


def init(sqluri='sqlite:////tmp/acr.db', fill=True):
    engine = create_engine(sqluri)
    Session.configure(bind=engine)
    mappings.Base.metadata.create_all(engine)

    if not fill:
        return

    session = Session()

    #
    # Cities
    #
    existing_hash = get_hash(session, u"city")
    cities = os.path.join(os.path.dirname(__file__), 'data',
                          'communes.csv')
    with open(cities) as f:
        file_hash = hashlib.md5(f.read()).hexdigest()

    if file_hash != existing_hash:
        done = []

        with open(cities, 'rb') as f:
            reader = csv.reader(f, delimiter='\t')
            for index, row in enumerate(reader):
                if index == 0:
                    continue
                label = unicode(row[1], 'utf8')
                zipcode = int(row[2])
                if (label, zipcode) in done:
                    continue
                city = mappings.City(label, zipcode)
                session.add(city)
                done.append((label, zipcode))

        session.commit()
        set_hash(session, u"city", file_hash)

    #
    # Members
    #
    existing_hash = get_hash(session, u"member")
    members = os.path.join(os.path.dirname(__file__), 'data',
                            'adherents.csv')

    with open(members) as f:
        file_hash = hashlib.md5(f.read()).hexdigest()

    if file_hash != existing_hash:

        with open(members, 'rb') as f:
            reader = csv.reader(f, delimiter=';')
            for index, row in enumerate(reader):
                if index in (0, 1):
                    continue
                row = [unicode(value, 'utf8') for value in row]

                member = mappings.Member()
                member.lastname = row[1]
                member.firstname = row[2]
                member.address = row[3]
                member.city_code = int(row[4])
                member.city_label = row[5]
                try:
                    member.phone = int(row[6].replace(' ', ''))
                except ValueError:
                    pass
                member.birthday = datetime.datetime.strptime(row[7],
                                                             '%m/%d/%y')

                #cat
                #email
                #type lice
                #numlic
                #date cert
                #pay
                #date maj

                session.add(member)


        set_hash(session, u"member", file_hash)



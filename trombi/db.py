# encoding: utf8
from datetime import datetime
import csv
import os
import hashlib
import locale

from passlib.hash import sha256_crypt
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from trombi import mappings


DATADIR = os.path.join(os.path.dirname(__file__), 'data')
session_factory = sessionmaker(autoflush=False)
Session = scoped_session(session_factory)
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')


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


def cvs2table(session, name, callback, delimiter=';'):
    existing_hash = get_hash(session, name)
    csvfile = os.path.join(DATADIR, u'%s.csv' % name)

    with open(csvfile) as f:
        file_hash = hashlib.md5(f.read()).hexdigest()

    if file_hash != existing_hash:
        with open(csvfile, 'rb') as f:
            reader = csv.reader(f, delimiter=delimiter)
            for index, row in enumerate(reader):
                obj = callback(index, row)
                if obj is not None:
                    session.add(obj)

        session.commit()
        set_hash(session, name, file_hash)


def init(sqluri='sqlite:////tmp/acr.db', fill=True):
    engine = create_engine(sqluri)
    session_factory.configure(bind=engine)
    mappings.Base.metadata.create_all(engine)

    if not fill:
        return

    session = Session()

    # Membership
    def _create_membership(index, row):
        if index == 0:
            return
        membership = mappings.Membership()
        membership.label = unicode(row[0], 'utf8')
        membership.price = int(row[1])
        return membership

    cvs2table(session, u"membership", _create_membership)

    # Categories
    def _create_cat(index, row):
        if index == 0:
            return
        cat = mappings.Category()
        cat.code = unicode(row[0], 'utf8')
        cat.label = unicode(row[1], 'utf8')
        cat.min_age = int(row[2])
        cat.max_age = int(row[3])
        return cat

    cvs2table(session, u"categories", _create_cat)

    # Cities
    done = []

    def _create_city(index, row):
        if index == 0:
            return
        label = unicode(row[1], 'utf8')
        zipcode = int(row[2])
        if (label, zipcode) in done:
            return
        city = mappings.City(label, zipcode)
        done.append((label, zipcode))
        return city

    cvs2table(session, u"communes", _create_city, delimiter='\t')

    # Members
    def _create_member(index, row):
        if index in (0, 1):
            return

        row = [unicode(value, 'utf8').strip() for value in row]
        if all(value == '' for value in row):
            return

        member = mappings.Member()
        member.permissions = "User"
        member.lastname = row[1]
        member.firstname = row[2]
        member.address = row[3]

        try:
            zipcode = int(row[4])
            label = row[5]
            if u'SAINT ' in label:  # XXX bof
                label = label.replace(u'SAINT', u'ST')

            res = session.query(mappings.City).filter_by(zipcode=zipcode,
                                                         label=label)
            city = res.one()
            if city:
                member.city = city

        except ValueError:
            pass

        member.phone = row[6].replace(' ', '')
        member.birthday = datetime.strptime(row[7], '%m/%d/%y')
        if member.birthday.year > 2016:

            member.birthday = datetime(member.birthday.year-100,
                                       member.birthday.month,
                                       member.birthday.day)

        if row[8] == u'S':
            member.category_code = u'SE'
        else:
            member.category_code = row[8]

        gender = row[9]
        if gender in (u'H', u'M'):
            gender = u'M'

        member.gender = gender
        member.email = row[10].replace(',', '.')

        try:
            price = float(row[14].replace(',', '.'))
            res = session.query(mappings.Membership).filter_by(price=price).first()
            if res:
                member.membership_label = res.label
            else:
                raise ValueError()
        except ValueError:
            label = row[11].split('\n')[-1]
            res = session.query(mappings.Membership).filter_by(label=label).first()
            if res:
                member.membership_label = label
            else:
                member.membership_label = u'Simple'
        member.licence = row[12]
        try:
            cert = datetime.strptime(row[13], '%m/%d/%y')
            member.medical_certificate_date = cert
        except ValueError:
            pass

        last_upd = row[-1].encode('utf8').lower().split('-')

        if last_upd[0] == 'fev':
            last_upd[0] = 'fév'

        if last_upd[0] == 'dec':
            last_upd[0] = 'déc'

        if last_upd[0] == 'sep':
            last_upd[0] = 'sept'

        try:
            member.last_updated = datetime.strptime('-'.join(last_upd), '%b-%y')
        except ValueError:
            pass
        member.is_published = member.has_paid = True    # XXX
        member.password = 'toto'    #sha256_crypt.encrypt('toto')
        return member

    cvs2table(session, u"adherents", _create_member)

    session.close()
    return engine

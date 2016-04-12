from wtforms_alchemy import ModelForm, QuerySelectField
from wtforms.fields import FormField

from trombi import mappings


def get_codes():
    from trombi.db import Session
    session = Session()
    return session.query(mappings.Category)


def get_city():
    from trombi.db import Session
    session = Session()
    sq = session.query(mappings.Member.city_id).distinct().subquery()
    return session.query(mappings.City).filter(mappings.City.id.in_(sq))


def get_city_label(city):
    return '%s (%s)' % (city.label, city.zipcode)


def get_membership():
    from trombi.db import Session
    session = Session()
    return session.query(mappings.Membership)


class CategoryForm(ModelForm):
    class Meta:
        model = mappings.Category
        include_primary_keys = True


class MembershipForm(ModelForm):
    class Meta:
        model = mappings.Membership
        include_primary_keys = True


class CityForm(ModelForm):
    class Meta:
        model = mappings.City


class MemberForm(ModelForm):
    class Meta:
        model = mappings.Member
        include_primary_keys = True

    category = QuerySelectField('category', query_factory=get_codes,
                                get_label='label')

    membership = QuerySelectField('membership', query_factory=get_membership,
                                  get_label='label')

    city = QuerySelectField('city', query_factory=get_city,
                            get_label=get_city_label)

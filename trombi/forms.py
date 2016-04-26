from collections import OrderedDict
from wtforms_alchemy import ModelForm, QuerySelectField
from wtforms import TextField
from wtforms.fields import FormField
from wtforms.widgets import Input, HTMLString

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


class BaseForm(ModelForm):
    def __iter__(self):
        field_order = getattr(self, 'field_order', None)
        if field_order:
            temp_fields = []
            for name in field_order:
                if name == '*':
                    for k, v in self._fields.items():
                        if k not in field_order:
                            temp_fields.append((k, v))
                    break
                else:
                    temp_fields.append((name, self._fields[name]))

            self._fields = OrderedDict(temp_fields)

        return super(BaseForm, self).__iter__()


class CategoryForm(BaseForm):
    class Meta:
        model = mappings.Category
        include_primary_keys = True


class MembershipForm(BaseForm):
    class Meta:
        model = mappings.Membership
        include_primary_keys = True


class CityForm(BaseForm):
    class Meta:
        model = mappings.City


class CityInput(Input):
    input_type = 'city'

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('type', self.input_type)

        if 'value' not in kwargs:
            kwargs['value'] = field._value()

        params = self.html_params(name=field.name, **kwargs)
        return HTMLString('<input %s/>' % params)


class CityField(TextField):
    widget = CityInput()



class MemberForm(BaseForm):
    class Meta:
        model = mappings.Member
        include_primary_keys = True

    category = QuerySelectField('category', query_factory=get_codes,
                                get_label='label')

    membership = QuerySelectField('membership', query_factory=get_membership,
                                  get_label='label')

    city = CityField('city')

    field_order = ('is_published', 'bio', 'email', 'phone', 'address', 'city',
                   '*')

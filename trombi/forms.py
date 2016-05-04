# encoding: utf8
from collections import OrderedDict
from wtforms_alchemy import (ModelForm, QuerySelectField,
                             DataRequired)
from wtforms import TextField
from wtforms.validators import EqualTo, Required
from wtforms.fields import FormField, PasswordField
from wtforms.widgets import Input, HTMLString

from trombi import mappings
from trombi.db import Session
from trombi.mappings import City


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

    def can_edit(self, member, field):
        return False


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


class ChangePassword(BaseForm):
  password = PasswordField('Mot de passe',
            [Required(), EqualTo('confirm',
               message=u'Les mots de passe diffèrent')])
  confirm  = PasswordField('Resaisir mot de passe')


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

    def validate(self, form, extra_validators=()):
        if isinstance(self.data, unicode):
            db = Session()
            city_data = self.data.split(u'(')
            if len(city_data) == 2:
                city = city_data[0].strip()
                zipcode = city_data[1].strip()[:-1]
                city = db.query(City).filter(City.zipcode==zipcode,
                                             City.label==city).first()
                if city:
                    self.data = city
                    return True
            self.errors = ['Unkown city']
            return False
        return True


class MemberForm(BaseForm):
    class Meta:
        model = mappings.Member
        include_primary_keys = False
        exclude = ['password']

    category = QuerySelectField('category', query_factory=get_codes,
                                get_label='label')

    membership = QuerySelectField('membership', query_factory=get_membership,
                                  get_label='label')

    city = CityField('city')

    field_order = ('is_published', 'bio', 'email', 'phone', 'phone2',
                   'address', 'city', '*')


    user_can_change = ['is_published', 'bio', 'email', 'phone', 'phone2',
                       'address', 'city']

    def can_edit(self, member, field):
        if member.is_super_user:
            return True

        if member.email != self.email.data:
            return False

        # that's my data !
        return field.name in self.user_can_change

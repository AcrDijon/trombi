import os
import json

from bottle import static_file, redirect, request, response
from bottle import route, app, request, post, get, auth_basic

from passlib.hash import sha256_crypt
from trombi.mappings import Member, City
from trombi import forms
from trombi.server import PICS, RESOURCES
from trombi.db import Session


def template(name, *args, **kw):
    if 'user' not in kw and hasattr(request, 'user'):
        kw['user'] = request.user

    return app.template(name, *args, **kw)


@route('/')
def index(db):
    return template("index")


@route('/member')
def members(db):
    letter = request.query.get('letter')
    members = db.query(Member)
    if letter is not None:
        members = members.filter(Member.lastname.like(u'%s%%' % letter))
    return template("members", members=members, letter=letter)


@route('/member/:id/edit')
def member_edit(id, db):
    member = db.query(Member).filter_by(id=id).one()
    form = forms.MemberForm(obj=member)
    return template("member_edit", form=form, member=member)


@post('/member/:id')
def member_post(id, db):
    member = db.query(Member).filter_by(id=id).one()

    if 'photo' in request.files:
        # XXX conversion + security
        photo = request.files['photo']
        filename = '%s-%s.jpg' % (member.firstname.lower(),
                                  member.lastname.lower())
        filename = os.path.join(PICS, filename)
        photo.save(filename, overwrite=True)

    post_data = request.POST.decode()
    form = forms.MemberForm(post_data, obj=member)

    if form.validate():
        form.populate_obj(member)

    return template("member_edit", form=form, member=member)



@route('/member/:id')
def member(id, db):
    member = db.query(Member).filter_by(id=id).one()
    return template("member", member=member)


@route("/resources/<filepath:path>")
def serve_resource(filepath):
    return static_file(filepath, root=RESOURCES)


@route("/pics/<filepath:path>")
def serve_static(filepath):
    if not os.path.exists(os.path.join(PICS, filepath)):
        filepath = 'empty.jpg'
    return static_file(filepath, root=PICS)


@route('/autocomplete/city')
def autocomplete(db):
    query = request.query.get('query')
    cities = db.query(City)
    if query:
        cities = cities.filter(City.label.like(u'%s%%' % query))

    cities = cities.limit(10)
    suggestions = []
    for city in cities:
        city = {'label': city.label, 'zipcode': city.zipcode,
                'value': '%s (%s)' % (city.label, city.zipcode),
                'data': city.id}

        suggestions.append(city)

    response.content_type = 'application/json'
    data = {'suggestions': suggestions}
    return json.dumps(data)


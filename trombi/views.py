# encoding: utf8
import os
import json
import csv
import StringIO

#import PIL
#from PIL import Image

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


@route('/admin')
def admin(db):
    return template("admin")


_HEADERS = ['lastname', 'firstname']


@route('/export')
def export(db):
    members = db.query(Member).order_by(Member.lastname)
    content = StringIO.StringIO()
    writer = csv.writer(content, delimiter=',')
    writer.writerow(_HEADERS)
    for member in members:
        writer.writerow([getattr(member, field).encode('utf8') for field in _HEADERS])

    response.headers['Content-Disposition'] = 'inline; filename="adherents-acr.csv"'
    response.content_type = 'text/csv'
    content.seek(0)
    return content.read()


@route('/member')
def members(db):
    letter = request.query.get('letter')
    members = db.query(Member)
    lastnames = members.distinct(Member.lastname)
    letters = []

    for member in lastnames:
        first = member.lastname.upper()[0]
        if first not in letters:
            letters.append(first)

    letters.sort()

    if letter is not None:
        members = members.filter(Member.lastname.like(u'%s%%' % letter))
    return template("members", members=members, letter=letter,
                    letters=letters)


@route('/member/:id/edit')
def member_edit(id, db):
    member = db.query(Member).filter_by(id=id).one()
    form = forms.MemberForm(obj=member)
    return template("member_edit", form=form, member=member)


@post('/member/:id')
def member_post(id, db):
    id = int(id)

    member = db.query(Member).filter_by(id=id).one()
    if not request.user.is_super_user and member.id != id:
        bottle.HTTPError(401, "Access denied")

    if 'photo' in request.files:
        # security
        photo = request.files['photo']
        filename = '%s-%s.jpg' % (member.firstname.lower(),
                                  member.lastname.lower())
        filename = os.path.join(PICS, filename)
        photo.save(filename, overwrite=True)

        # resizing if needed
        #img = Image.open(filename)
        #import pdb; pdb.set_trace()
        #img = img.resize((200, 200),PIL.Image.ANTIALIAS)
        #img.save(filename)


    post_data = request.POST.decode()
    if 'password' in post_data and post_data['password'] == '':
        del post_data['password']

    if not request.user.is_super_user and member.id == id:
        for field in list(post_data.keys()):
            if field not in forms.MemberForm.user_can_change:
                del post_data[field]

    form = forms.MemberForm(post_data, obj=member)

    if form.validate():
        form.populate_obj(member)

    return template("member_edit", form=form, member=member)



@route('/member/:id')
def member(id, db):
    id = int(id)
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


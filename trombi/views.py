# encoding: utf8
import os
import json
import csv
import StringIO
import cgi

import PIL
from PIL import Image

import bottle
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
        alert = u'Page non authorisée'
        return redirect("/login?alert=%s" % alert.encode('base64'))

    if 'photo' in request.files:
        # security
        photo = request.files['photo']
        filename = '%s-%s.jpg' % (member.firstname.lower(),
                                  member.lastname.lower())
        filename = os.path.join(PICS, filename)
        photo.save(filename, overwrite=True)

        # resizing if needed
        img = Image.open(filename)
        if img.width != 200 or img.height != 200:
            img = img.resize((200, 200), PIL.Image.ANTIALIAS)
            img.save(filename)


    post_data = request.POST.decode()
    if 'password' in post_data and post_data['password'] == '':
        del post_data['password']

    if not request.user.is_super_user and member.id == id:
        for field in list(post_data.keys()):
            if field not in forms.MemberForm.user_can_change:
                del post_data[field]

    form = forms.MemberForm(post_data, obj=member)

    if form.validate():
        for field in form:
            if field.name not in post_data.keys():
                del form[field.name]
        form.populate_obj(member)

    return template("member_edit", form=form, member=member)



@route('/member/:id')
def member(id, db):
    id = int(id)

    if hasattr(request, 'user'):
        my_page = request.user.id == id
        super_user = request.user.is_super_user
    else:
        my_page = False
        super_user = False

    member = db.query(Member).filter_by(id=id).one()
    if (my_page or super_user) or member.is_published:
        return template("member", member=member)
    else:
        alert = u'Page non authorisée'
        return redirect("/login?alert=%s" % alert.encode('base64'))


@route("/resources/<filepath:path>")
def serve_resource(filepath):
    return static_file(filepath, root=RESOURCES)


@route("/pics/<filepath:path>")
def serve_static(filepath):
    if not os.path.exists(os.path.join(PICS, filepath)):
        return redirect('/pics/empty.jpg')

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


@bottle.error(404)
def error404(error):
    return template("404")


#
# move to AuthPlugin
#

# XXX how can I ca get ridd of those... (AuthPlugin handles it)
@post('/login')
def post_login():
    return


@route('/logout')
def logout():
    pass

@route('/login')
def login():
    alert = request.params.get('alert')
    if alert:
        alert = alert.decode('base64')
        # avoid XSS attacks
        alert = cgi.escape(alert)

    email = request.params.get('email')
    if email is None:
        if hasattr(request, 'user'):
            email = request.user.email
        else:
            session = request.environ['beaker.session']
            email = session.get('email', '')
    else:
        email = email.decode('base64')
        email = cgi.escape(email)

    from_url = request.params.get('from_url')
    if from_url:
        from_url = cgi.escape(from_url.decode('base64'))

    return template("login", email=email, alert=alert, from_url=from_url)


@route('/reset')
def reset():
    email = request.params.get('email')
    if email is None:
        if hasattr(request, 'user'):
            email = request.user.email
        else:
            session = request.environ['beaker.session']
            email = session.get('email', '')
    else:
        email = email.decode('base64')
        email = cgi.escape(email)

    return template("reset_password", email=email)


@post('/reset')
def post_reset():
    return


@route('/change_password')
def change_password():
    form = forms.ChangePassword()
    return template("change_password", form=form)


@post('/change_password')
def post_change_password():
    post_data = request.POST.decode()
    form = forms.ChangePassword(post_data)

    if form.validate():
        request.user.password = form.password.data
        alert = 'Mot de passe modifié'
        return redirect('/logout?alert=%s' % alert.encode('base64'))

    return template("change_password", form=form)

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
from sqlalchemy.orm.exc import NoResultFound

from passlib.hash import sha256_crypt
from trombi.mappings import Member, City
from trombi import forms
from trombi.server import PICS, RESOURCES, raise_401
from trombi.db import Session


def template(name, *args, **kw):
    if 'user' not in kw and hasattr(request, 'user'):
        kw['user'] = request.user

    alert = request.params.get('alert')
    if alert:
        alert = alert.decode('base64')
        # avoid XSS attacks
        alert = cgi.escape(alert)

    kw['alert'] = alert
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
        if first not in letters and (member.is_published
                or request.user.is_super_user):
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

        # cropping
        img = Image.open(filename)
        x = int(request.POST.get('x', 0))
        y = int(request.POST.get('y', 0))
        w = int(request.POST.get('w', 0))
        h = int(request.POST.get('h', 0))
        img = img.crop((x, y, x + w, y + h))
        img.save(filename)

        # resizing if needed
        img = Image.open(filename)
        current_w, current_h = img.size

        if current_w != 200 or current_h != 200:
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
        # we've validated the data
        for field in form:
            if field.name not in post_data.keys():
                del form[field.name]

        form.populate_obj(member)

        # let's redirect
        return redirect('/member/%s' % str(id))

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

    login = request.params.get('login')
    if login is None:
        if hasattr(request, 'user'):
            login = request.user.login
        else:
            session = request.environ['beaker.session']
            login = session.get('login', '')
    else:
        login = login.decode('base64')
        login = cgi.escape(login)

    from_url = request.params.get('from_url')
    if from_url:
        from_url = cgi.escape(from_url.decode('base64'))

    return template("login", login=login, from_url=from_url)


@route('/reset')
def reset():
    login = request.params.get('login')
    if login is None:
        if hasattr(request, 'user'):
            login = request.user.login
        else:
            session = request.environ['beaker.session']
            login = session.get('login', '')
    else:
        login = login.decode('base64')
        login = cgi.escape(login)

    return template("reset_password", login=login)


@post('/reset')
def post_reset(db):
    # we generate a unique token and send it by e-mail to the user
    # of course, if the mail is intercepted or the server is not in HTTPS
    # that's a security breach.
    login = request.POST.get('login')
    try:
        member = db.query(Member).filter_by(login=login).one()
    except NoResultFound:
        alert = 'Utilisateur Inconnu.'
        return redirect('/?alert=%s' % alert.encode('base64'))

    member.send_reset_email()
    alert = 'Vous allez reçevoir un e-mail.'
    return redirect('/?alert=%s' % alert.encode('base64'))


def _auth_by_token(db):
    if not hasattr(request, 'user'):
        token = request.GET.get('token')
        if token is None:
            token = request.POST.get('token')

        login = request.GET.get('login')
        if login is None:
            login = request.POST.get('login')

        if token is None or login is None:
            return raise_401(alert='Accès interdit')

        member = db.query(Member).filter_by(login=login).one()

        if member.token != token:
            return raise_401(alert=u'Mauvais token')

        request.user = member
    else:
        login = request.user.login
        token = request.user.token

    return token, login


@route('/change_password')
def change_password(db):
    form = forms.ChangePassword()
    token, login = _auth_by_token(db)
    form.token.data = token
    form.login.data = login
    return template("change_password", form=form)


@post('/change_password')
def post_change_password(db):
    token, login = _auth_by_token(db)
    post_data = request.POST.decode()
    form = forms.ChangePassword(post_data)

    if form.validate():
        request.user.password = form.password.data
        request.user.token = ''
        alert = 'Mot de passe modifié'
        return redirect('/logout?alert=%s' % alert.encode('base64'))

    return template("change_password", form=form)

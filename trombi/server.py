from functools import partial
import os
import time
from urllib import urlencode

import bottle
from bottle import route, app as app_stack, view, template, request, redirect
from bottle.ext.sqlalchemy import SQLAlchemyPlugin
from sqlalchemy.orm import scoped_session
from passlib.hash import sha256_crypt
from beaker.middleware import SessionMiddleware

from trombi.db import init, Session
from trombi.mappings import Base, Member
from trombi import forms
from trombi.translate import _


HERE = os.path.dirname(__file__)
TEMPLATES = os.path.join(HERE, 'templates')
bottle.TEMPLATE_PATH.append(TEMPLATES)
PICS = os.path.join(HERE, 'photos')
RESOURCES = os.path.join(HERE, 'resources')

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}


class AuthPlugin(object):

    AUTHORIZED_PATH = ['/', '/login', '/logout']
    ASSETS = '/resources/'

    def __init__(self, app, engine, create_session):
        self.engine = engine
        self.app = app
        self.create_session = create_session
        self._cache = {}

    def _401(self, alert=None, email=None):
        url = request.urlparts
        from_url = url.path
        params = {}

        if url.query:
            from_url += '?' + url.query
        if url.fragment:
            from_url += '#' + url.fragment

        params['from_url'] = from_url.encode('base64').strip()

        if alert is not None:
            params['alert'] = alert.encode('base64').strip()

        if email is not None:
            params['email'] = email.encode('base64').strip()

        params = urlencode(params)
        return redirect("/login?" + params)

    def _get_member(self, email, password=None):
        db = self.create_session(self.engine)
        member = db.query(Member).filter_by(email=email).first()
        if member is None:
            return self._401(u'Utilisateur inconnu')

        # verify the password
        if password is not None:
            hashed = member.password.hash
            if hashed in self._cache:
                if self._cache[hashed] != password:
                    return self._401(u'Mauvais mot de passe', email=email)
            else:
                if not sha256_crypt.verify(password, hashed):
                    return self._401(u'Mauvais mot de passe', email=email)
                self._cache[hashed] = password

        return member

    def _anonymous_ok(self):
        return (request.path in self.AUTHORIZED_PATH or
                request.path.startswith(self.ASSETS))

    def apply(self, callback, context):
        def wrapper(*args, **kwargs):
            session = request.environ['beaker.session']

            # login out
            if request.path == '/logout':
                session['email'] = None
                session.delete()
                return redirect('/')

            # login in
            if request.path == '/login' and request.method == 'POST':
                email = request.POST['email']
                password = request.POST['password']
                member = self._get_member(email, password)
                session['email'] = email
                session.save()
                from_url = request.POST.get('from_url', '/')
                return redirect(from_url)

            # grab the connected user
            email = session.get('email', None)

            if not email and not self._anonymous_ok():
                # not connected, and needs it
                return self._401("Cette page necessite une connexion")

            if email:
                bottle.request.user = self._get_member(email)

            return callback(*args, **kwargs)

        return wrapper


def make_app():
    def create_session(*args, **kw):
        return Session

    app = bottle.app()
    app = SessionMiddleware(app, session_opts)
    engine = init()
    engine.echo = True
    bottle.install(SQLAlchemyPlugin(engine,
                   create_session=create_session))
    bottle.install(AuthPlugin(app, engine, create_session=create_session))
    app_stack.vars = {'_': _, 'time': time}
    app_stack.view = partial(view, **app_stack.vars)
    app_stack.template = partial(template, **app_stack.vars)
    from trombi import views
    return app


def main():
    app = make_app()
    bottle.debug(True)
    bottle.run(app=app, reloader=True)


if __name__ == '__main__':
    main()

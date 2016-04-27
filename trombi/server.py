from functools import partial
import os
import time

import bottle
from bottle import route, app as app_stack, view, template
from bottle.ext.sqlalchemy import SQLAlchemyPlugin
from sqlalchemy.orm import scoped_session
from passlib.hash import sha256_crypt

from trombi.db import init, Session
from trombi.mappings import Base, Member
from trombi import forms
from trombi.translate import _


HERE = os.path.dirname(__file__)
TEMPLATES = os.path.join(HERE, 'templates')
bottle.TEMPLATE_PATH.append(TEMPLATES)
PICS = os.path.join(HERE, 'photos')
RESOURCES = os.path.join(HERE, 'resources')


class AuthPlugin(object):

    def __init__(self, engine, create_session):
        self.engine = engine
        self.create_session = create_session
        self._cache = {}

    def _401(self):
        realm = "private"
        text = "Access denied"
        err = bottle.HTTPError(401, text)
        err.add_header('WWW-Authenticate', 'Basic realm="%s"' % realm)
        raise err

    def apply(self, callback, context):
        def wrapper(*args, **kwargs):
            auth = bottle.request.auth
            if auth is None:
                return self._401()

            email, password = auth
            db = self.create_session(self.engine)
            member = db.query(Member).filter_by(email=email).first()
            if member is None:
                return self._401()

            # verify the password
            hashed = member.password.hash
            if hashed in self._cache:
                if self._cache[hashed] != password:
                    return self._401()
            else:
                if not sha256_crypt.verify(password, hashed):
                    return self._401()
                self._cache[hashed] = password

            bottle.request.user = member
            return callback(*args, **kwargs)

        return wrapper


def make_app():
    def create_session(*args, **kw):
        return Session

    app = bottle.app()
    engine = init()
    engine.echo = True
    bottle.install(SQLAlchemyPlugin(engine,
                   create_session=create_session))
    bottle.install(AuthPlugin(engine, create_session=create_session))
    app_stack.vars = {'_': _, 'time': time}
    app_stack.view = partial(view, **app_stack.vars)
    app_stack.template = partial(template, **app_stack.vars)
    from trombi import views
    return app


def main():
    make_app()
    bottle.debug(True)
    bottle.run(reloader=True)


if __name__ == '__main__':
    main()

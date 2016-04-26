from functools import partial
import os
import time

import bottle
from bottle import route, app as app_stack, view, template
from bottle.ext.sqlalchemy import SQLAlchemyPlugin
from sqlalchemy.orm import scoped_session

from trombi.db import init, Session
from trombi.mappings import Base, Member
from trombi import forms
from trombi.translate import _


HERE = os.path.dirname(__file__)
TEMPLATES = os.path.join(HERE, 'templates')
bottle.TEMPLATE_PATH.append(TEMPLATES)
PICS = os.path.join(HERE, 'photos')
RESOURCES = os.path.join(HERE, 'resources')


def make_app():
    def create_session(*args, **kw):
        return Session

    app = bottle.app()
    engine = init()
    engine.echo = True
    bottle.install(SQLAlchemyPlugin(engine,
                   create_session=create_session))
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

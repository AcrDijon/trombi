from functools import partial
import os
import bottle
from bottle import route, app as app_stack, view, template
from bottle.ext.sqlalchemy import SQLAlchemyPlugin

from trombi.db import init, Session
from trombi.mappings import Base, Member
from trombi import forms

HERE = os.path.dirname(__file__)
TEMPLATES = os.path.join(HERE, 'templates')
bottle.TEMPLATE_PATH.append(TEMPLATES)
PICS = os.path.join(HERE, 'photos')
RESOURCES = os.path.join(HERE, 'resources')


def make_app():
    app = bottle.app()
    engine, session = init()
    bottle.install(SQLAlchemyPlugin(engine, Base.metadata, create=True,
                                create_session=Session))

    app_stack.vars = {}
    app_stack.view = partial(view, **app_stack.vars)
    app_stack.template = partial(template, **app_stack.vars)
    app_stack.session = session
    from trombi import views
    return app


def main():
    make_app()
    bottle.debug(True)
    bottle.run(reloader=True)


if __name__ == '__main__':
    main()

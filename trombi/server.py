from functools import partial
import os
import bottle
from bottle import route, app, view, template
from bottle.ext.sqlalchemy import SQLAlchemyPlugin

from trombi.db import init, Session
from trombi.mappings import Base, Member
from trombi import forms

HERE = os.path.dirname(__file__)
TEMPLATES = os.path.join(HERE, 'templates')
bottle.TEMPLATE_PATH.append(TEMPLATES)
PICS = os.path.join(HERE, 'photos')
RESOURCES = os.path.join(HERE, 'resources')



def main():
    engine, session = init()
    bottle.install(SQLAlchemyPlugin(engine, Base.metadata, create=True,
                                create_session=Session))

    app.vars = {}
    app.view = partial(view, **app.vars)
    app.template = partial(template, **app.vars)
    app.session = session

    from trombi import views
    bottle.debug(True)
    bottle.run(reloader=True)


if __name__ == '__main__':
    main()

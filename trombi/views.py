import os

from bottle import static_file
from bottle import route, app, request

from trombi.mappings import Member
from trombi import forms
from trombi.server import PICS, RESOURCES


@route('/')
def index(db):
    return app.template("index")


@route('/member')
def members(db):
    # XXX security
    letter = request.query.get('letter', 'A')
    members = db.query(Member).filter(Member.lastname.like(u'%s%%' % letter))
    return app.template("members", members=members, letter=letter)


@route('/member/:id/edit')
def member_edit(id, db):
    member = db.query(Member).filter_by(id=id).one()
    form = forms.MemberForm(obj=member)
    return app.template("member", form=form, member=member)


@route('/member/:id')
def member(id, db):
    member = db.query(Member).filter_by(id=id).one()
    return app.template("member", member=member)


@route("/resources/<filepath:path>")
def serve_resource(filepath):
    return static_file(filepath, root=RESOURCES)

@route("/pics/<filepath:path>")
def serve_static(filepath):
    if not os.path.exists(os.path.join(PICS, filepath)):
        filepath = 'empty.jpg'
    return static_file(filepath, root=PICS)

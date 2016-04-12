from bottle import route, app
from trombi.mappings import Member
from trombi import forms


@route('/')
def index(db):
    return app.template("index")


@route('/member')
def members(db):
    members = db.query(Member)
    return app.template("members", members=members)


@route('/member/:id')
def member(id, db):
    member = db.query(Member).filter_by(id=id).one()
    form = forms.MemberForm(obj=member)
    return app.template("member", form=form)

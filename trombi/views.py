from bottle import route, app
from trombi.mappings import Member
from trombi import forms


@route('/')
def listing(db):
    members = db.query(Member)
    tmp = '<li><a href="/member/%s">%s</a></li>'
    result = "".join([tmp % (member.id, member.lastname) for member in members])
    return "<ul>%s</ul>" % (result)


@route('/member/:id')
def member(id, db):
    member = db.query(Member).filter_by(id=id).one()
    form = forms.MemberForm(obj=member)
    return app.template("member", form=form)

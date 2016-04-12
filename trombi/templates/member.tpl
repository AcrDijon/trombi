% rebase('base.tpl', title='%s %s' % (form.firstname.object_data, form.lastname.object_data))

<h1>{{form.firstname.object_data}} {{form.lastname.object_data}}</h1>

<form method="POST" action="/member/{{!form.id.object_data}}">
 % for field in form:
  % if field.name != 'id':
    <div>{{!field.label }}: {{!field()}}</div>
  % end
 % end
</form>



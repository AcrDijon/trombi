
<div class="page-header">
  <h1>{{member.firstname.capitalize()}} {{member.lastname.capitalize()}}</h1>
</div>

<div class="row">

<form role="form" method="POST" action="/member/{{!form.id.object_data}}">
 % for field in form:
  % if field.name != 'id':
    <div class="form-group">
      {{!field.label}}
      {{!field()}}
    </div>
  % end
 % end
 <hr/>
 <button type="submit" class="btn btn-default">Submit</button>
</form>


</div>

% rebase('base.tpl', title='%s %s' % (member.firstname.capitalize(), member.lastname.capitalize()))

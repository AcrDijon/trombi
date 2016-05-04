% rebase('base.tpl', title='ACR Dijon')

<div class="page-header">
<h1>Changer le mot de passe</h1>
</div>

<form class="form-horizontal"
      role="form"
      method="POST"
      action="/change_password">

 % for field in form:
       % if field.errors:
       <div class="form-group has-error">
       % else:
       <div class="form-group">
       % end
       % if field.type != 'HiddenField':
         <label for="{{ field.id }}" class="control-label col-sm-2">
             {{_(field.label.text)}}
         </label>
       % end
       <div class="col-sm-10">
       {{ !field(class_='form-control') }}
       </div>
       % if field.errors:
         % for e in field.errors:
          <p class="help-block">{{ e }}</p>
         % end
       % end
       </div>
 % end
 <hr/>
 <button type="submit" class="btn btn-default">Changer</button>

</form>



<div class="page-header">
  <h1>{{member.firstname.capitalize()}} {{member.lastname.capitalize()}}</h1>
</div>

<div class="row">

<form class="form-horizontal"  role="form" method="POST" action="/member/{{!form.id.object_data}}">
 % for field in form:
  % if field.name != 'id':
     % if field.errors:
     <div class="form-group has-error">
     % else:
     <div class="form-group">
     % end
        % if field.type != 'HiddenField':
            <label for="{{ field.id }}" class="control-label col-sm-2">{{field.label.text}}</label>
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
 % end
 <hr/>
 <button type="submit" class="btn btn-default">Submit</button>
</form>


</div>
<script src="/resources/js/bootstrap-datepicker.js"></script>

<script src="/resources/js/bootstrap-datepicker.fr.min.js" charset="UTF-8"></script>

<script>
 $('#birthday').datepicker({
   format: "yyyy-mm-dd",
   language: "fr"
 });

 $('#medical_certificate_date').datepicker({
   format: "yyyy-mm-dd",
   language: "fr"
 });

 $('#last_updated').datepicker({
   format: "yyyy-mm-dd",
   language: "fr"
 });

</script>


% rebase('base.tpl', title='%s %s' % (member.firstname.capitalize(), member.lastname.capitalize()))

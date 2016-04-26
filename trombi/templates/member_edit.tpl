
<div class="page-header">
  <h1>{{member.firstname.capitalize()}} {{member.lastname.capitalize()}}</h1>
</div>

<div class="row">

<form enctype='multipart/form-data'
      class="form-horizontal"
      role="form"
      method="POST"
      action="/member/{{!form.id.object_data}}">

  <div class="form-group">
    <label for="photo" class="control-label col-sm-2">Photo</label>
    <div class="col-sm-10">
      <img
src="/pics/{{member.firstname.lower()}}-{{member.lastname.lower()}}.jpg?q={{time.time()}}"/>
      <div class="photoChanger">
      <span class="btn btn-default btn-file">
         <span id="fileTitle">Changer la photo</span>
         <input type="file" id="photo" name="photo"/>
      </span>
      </div>
    </div>
  </div>

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
 <button type="submit" class="btn btn-default">Submit</button>
</form>


</div>
<script src="/resources/js/bootstrap-datepicker.js"></script>
<script src="/resources/js/jquery.autocomplete.js"></script>
<script src="/resources/js/bootstrap-datepicker.fr.min.js" charset="UTF-8"></script>

<script>
$(document).on('change', '.btn-file :file', function() {
  var input = $(this),
  numFiles = input.get(0).files ? input.get(0).files.length : 1,
  label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
  input.trigger('fileselect', [numFiles, label]);
});

$(document).ready( function() {
  $('.btn-file :file').on('fileselect', function(event, numFiles, label) {
    console.log(numFiles);
    $('#fileTitle').text(label);
  });

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

 $('#city').autocomplete({
    serviceUrl: '/autocomplete/city',
    onSelect: function (suggestion) {
    }
 });

});

</script>


% rebase('base.tpl', title='%s %s' % (member.firstname.capitalize(), member.lastname.capitalize()))

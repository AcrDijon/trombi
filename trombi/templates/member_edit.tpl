
<div class="page-header">
  <h1>{{member.display_name()}}</h1>
</div>


<form enctype='multipart/form-data'
      class="form-horizontal"
      role="form"
      method="POST"
      action="/member/{{member.id}}">

  <input type="hidden" id="x" name="x" value="0"/>
  <input type="hidden" id="y" name="y" value="0"/>
  <input type="hidden" id="w" name="w" value="200"/>
  <input type="hidden" id="h" name="h" value="200"/>

  <div class="form-group">
    <label for="photo" class="control-label col-sm-2">Photo</label>
    <div class="col-sm-10">
      <img   src="{{member.picture()}}?q={{time.time()}}"
             id="memberPic" >

      <div class="photoChanger">
      <span class="btn btn-default btn-file">
         <span id="fileTitle">Changer la photo</span>
         <input type="file" id="photo" name="photo" accept=".jpeg,.jpg" />
      </span>
      </div>
    </div>
  </div>

 % for field in form:
     % if user.is_super_user or form.can_edit(member, field):
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
 % end
 <hr/>
 <button type="submit" class="btn btn-default">Valider</button>
</form>


<script src="/resources/js/jquery.Jcrop.min.js"></script>
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
  var jcrop_api = null;

  function updateCoords(c) {
    jQuery('#x').val(c.x);
    jQuery('#y').val(c.y);
    jQuery('#w').val(c.w);
    jQuery('#h').val(c.h);
  };

  $('#photo').change(function(){
    if (jcrop_api) {
      jcrop_api.destroy();
    }
    var url = $(this).val();
    var ext = url.substring(url.lastIndexOf('.') + 1).toLowerCase();
    var input = $(this);
    var numFiles = input.get(0).files ? input.get(0).files.length : 1;

    if (numFiles > 0) {
        var reader = new FileReader();
        reader.onload = function (e) {
           $('#memberPic').attr('src', e.target.result);
           $('#memberPic').Jcrop({aspectRatio: 1, setSelect: [0, 0, 200, 200], onSelect: updateCoords}, function () {
             jcrop_api = this;
           });
        }
       reader.readAsDataURL(input.get(0).files[0]);
    }
  });

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

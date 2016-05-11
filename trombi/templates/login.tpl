% rebase('base.tpl', title='ACR Dijon')

<div class="page-header">
<h1>Authentification</h1>
</div>

<form class="form-horizontal"
      role="form"
      method="POST"
      action="/login">
%if from_url:
  <input type="hidden" name="from_url" value="{{from_url}}"/>
% end
  <div class="form-group">
      <label for="login" class="control-label col-sm-2">Identifiant</label>
      <div class="col-sm-10">
        <input class="form-control" id="login" name="login"
               value="{{login}}" type="login">
      </div>
  </div>
  <div class="form-group">
      <label for="password" class="control-label col-sm-2">Mot de passe</label>
      <div class="col-sm-10">
        <input class="form-control" id="password" name="password"
               value="" type="password">
      </div>
  </div>

 <hr/>
  <button type="submit" class="btn btn-primary">Valider</button>
  <a class="btn btn-info" href="/reset" role="button">Mot de passe perdu?</a>
</form>


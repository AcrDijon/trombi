% rebase('base.tpl', title='ACR Dijon')

<div class="page-header">
<h1>Authentification</h1>
</div>

% if alert:
<div class="alert alert-warning" role="alert">{{alert}}</div>
% end

<form class="form-horizontal"
      role="form"
      method="POST"
      action="/login">
%if from_url:
  <input type="hidden" name="from_url" value="{{from_url}}"/>
% end
  <div class="form-group">
      <label for="email" class="control-label col-sm-2">Couriel</label>
      <div class="col-sm-10">
        <input class="form-control" id="email" name="email"
               value="{{email}}" type="email">
      </div>
  </div>
  <div class="form-group">
      <label for="email" class="control-label col-sm-2">Mot de passe</label>
      <div class="col-sm-10">
        <input class="form-control" id="password" name="password"
               value="" type="password">
      </div>
  </div>

 <hr/>
  <button type="submit" class="btn btn-primary">Valider</button>
  <a class="btn btn-info" href="/reset" role="button">Mot de passe perdu?</a>
</form>


% rebase('base.tpl', title='ACR Dijon')

<div class="page-header">
<h1>Mot de passe perdu <small>Pas de panique!</small></h1>
</div>


<form class="form-horizontal"
      role="form"
      method="POST"
      action="/reset">
  <div class="form-group">
      <label for="login" class="control-label col-sm-2">Identifiant</label>
      <div class="col-sm-10">
        <input class="form-control" id="login" name="login"
               value="{{login}}" type="login">
       <span id="helpBlock" class="help-block">
Si vous avez perdu votre mot de passe, veuillez saisir votre identifiant
pour le re-initialiser. Vous reçevrez un e-mail pour vous guider.
</span>

      </div>
  </div>

 <hr/>
  <button type="submit" class="btn btn-primary">Valider</button>
</form>


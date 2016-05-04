% rebase('base.tpl', title='ACR Dijon')

<div class="page-header">
<h1>Mot de passe perdu <small>Pas de panique!</small></h1>
</div>


<form class="form-horizontal"
      role="form"
      method="POST"
      action="/reset">
  <div class="form-group">
      <label for="email" class="control-label col-sm-2">Couriel</label>
      <div class="col-sm-10">
        <input class="form-control" id="email" name="email"
               value="{{email}}" type="email">
       <span id="helpBlock" class="help-block">
Si vous avez perdu votre mot de passe, veuillez saisir votre e-mail
pour le re-initialiser. Vous reçevrez un e-mail pour pour guider.
</span>

      </div>
  </div>

 <hr/>
  <button type="submit" class="btn btn-primary">Valider</button>
</form>


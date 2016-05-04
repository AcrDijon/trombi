% rebase('base.tpl', title='ACR Dijon')

<div class="page-header">
<h1>ACR Dijon <small>Trombinoscope</small></h1>
</div>

<div class="jumbotron">
  <h1>Bienvenue!</h1>
<p>
Cet espace contient la liste des membres de l'ACR.
</p>

<p>
Si vous êtes un membre de l'ACR, vous pouvez modifier certaines de vos informations
personnelles sur votre fiche, mettre à jour votre bio, votre adresse, et
rendre public votre photo, bio et contact.
</p>

<p>
Vous pouvez aussi mettre un nom sur un visage, et lire les bio des autres membres.
</p>

% if defined('user'):
<p><a class="btn btn-primary btn-lg" href="/member/{{user.id}}" role="button">Ma Fiche</a></p>
% else:
<p><a class="btn btn-primary btn-lg" href="/login" role="button">Se connecter</a></p>
% end

</div>



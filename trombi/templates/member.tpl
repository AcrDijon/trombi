
<div class="page-header">
  <h1>{{member.firstname.capitalize()}} {{member.lastname.capitalize()}}
  <small>{{member.category.label}}</small>
  </h1>
</div>

<div class="row">

 <div class="col-xs-12 col-sm-3">
  <a href="#" class="thumbnail">
    <img src="/pics/{{member.firstname.lower()}}-{{member.lastname.lower()}}.jpg"/>
  </a>
 </div>
   % if member.bio:
 <div class="col-xs-12 col-sm-9" style="font-size: 150%">
  <div class="panel panel-default">
    <div class="panel-heading">
      <h3 class="panel-title">Bio</h3>
    </div>

    <div class="panel-body">
    <p>{{!member.bio}}</p>
   </div>
   </div>
   </div>
   % end
   <div class="col-xs-12 col-sm-9">
  <div class="panel panel-default">
    <div class="panel-heading">
      <h3 class="panel-title">Contacter</h3>
    </div>
    <div class="panel-body">
   <div>
     Couriel <a href="mailto:{{member.email}}"><strong>{{member.email}}</strong></a>
   </div>
   <div>
     Téléphone <strong>{{member.phone}}</strong>
   </div>
   % if member.phone2:
   <div>
     Téléphone #2 <strong>{{member.phone2}}</strong>
   </div>
   % end
 </div>
 </div>
 </div>

<div class="col-xs-12 col-sm-9">
  %if user.id == member.id  or user.is_super_user:
  <a class="btn btn-default" role="button"
     href="/member/{{member.id}}/edit">Modifier les infos</a>
  %end
</div>

</div>

% rebase('base.tpl', title='%s %s' % (member.firstname.capitalize(), member.lastname.capitalize()))

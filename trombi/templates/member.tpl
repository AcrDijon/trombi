
<div class="page-header">
  <a class="memberEdit" href="/member/{{member.id}}/edit">Modifier</a>
  <h1>{{member.firstname.capitalize()}} {{member.lastname.capitalize()}}</h1>
</div>

<div class="row">

 <div class="col-xs-2">
  <img src="/pics/{{member.firstname.lower()}}-{{member.lastname.lower()}}.jpg"/>
 </div>
 <div class="col-xs-8">
   <div>
     Email <a href="mailto:{{member.email}}"><strong>{{member.email}}</strong></a>
   </div>
   <div>
     Téléphone <strong>{{member.phone}}</strong>
   </div>
   <div>
     Licence <strong>{{member.licence}}</strong>
   </div>
   <div>
     Catégorie <strong>{{member.category.label}}</strong>
   </div>
   <div>
     Adresse <strong>{{member.address}} - {{member.city.label}} ({{member.city.zipcode}})</strong>
   </div>

  </div>

% rebase('base.tpl', title='%s %s' % (member.firstname.capitalize(), member.lastname.capitalize()))

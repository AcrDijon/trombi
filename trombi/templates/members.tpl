% rebase('base.tpl', title='Members' )

<div class="page-header">
  <h1>Liste des Adhérents <small>par ordre alphabétique</small></h1>
</div>


<nav>
  <ul class="pagination">
%if not letter:
<li class="active">
% else:
<li>
% end
<a href="/member">Tous</a>
</li>
% for c in letters:
% if c == letter:
    <li class="active">
% else:
    <li>
% end
<a href="/member?letter={{c}}">{{c}}</a></li>
% end
  </ul>
</nav>


<div class="grid">
  % for member in members:
    % if user.is_super_user or member.is_published:
    <div class="grid-item">
     <div class="grid-item-content">
      <a href="/member/{{member.id}}" class="thumbnail">
       <img src="/pics/{{member.firstname.lower()}}-{{member.lastname.lower()}}.jpg"/>
      </a>
      <span class="imagetext label label-default">{{member.firstname.capitalize()}} {{member.lastname.capitalize()}}</span>
     </div>
    </div>
    % end
  % end
</div>

<script src="/resources/js/masonry.pkgd.min.js">></script>

<script>

$(window).load(function() {
  $('.grid').masonry({
    itemSelector: '.grid-item',
    columnWidth: 209,  //'.grid-sizer',
    percentPosition: true
 });
});
</script>


% rebase('base.tpl', title='Members' )

<div class="page-header floaty">

<div id="letters">
% for c in [chr(l) for l in range(65, 91)]:
  % if c == letter:
    {{c}}
  % else:
    <a href="/member?letter={{c}}">{{c}}</a>
  % end
% end
</div>

  <h1>Liste des membres</h1>
  <div style="clear:both"></div>
</div>

<div class="container-fluid">
<div class="grid">
<div class="grid-sizer col-xs-3"></div>
 % for member in members:
 <div class="grid-item">
 <div class="grid-item-content">
   <a href="/member/{{member.id}}">
   <img src="/pics/{{member.firstname.lower()}}-{{member.lastname.lower()}}.jpg"/>
  </a>
   <span class="imagetext">{{member.firstname.capitalize()}} {{member.lastname.capitalize()}}</span>
 </div>
 </div>
% end

</div>
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


% rebase('base.tpl', title='Members' )

<h1>Members</h1>

<ul>
  %for member in members:
  <li>
    <a href="/member/{{member.id}}">{{member.firstname}} {{member.lastname}}</a>
  </li>
  %end
</ul>

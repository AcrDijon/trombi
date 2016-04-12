% rebase('base.tpl', title='Members' )

<h1>List des membres</h1>

<ul>
  %for member in members:
  <li>
    <a href="/member/{{member.id}}">{{member.firstname}} {{member.lastname}}</a>
  </li>
  %end
</ul>

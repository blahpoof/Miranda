<ul style="list-style-type:none; margin:0; padding:0;">	
	<li><a href="/">Home</a></li>
	%if signed_in:
		<li>{{email}}</li>
		<li><a href="/signout">Sign Out</a></li>
	%end
	%if not signed_in:
		<li><a href="/login">Sign in</a></li>
	%end
</ul>


<img src="logo.png">

<form action='/', method="GET">
	Keyword: <input name="keywords" type="text"/>
	<input value="Submit" type="submit"/>
</form>
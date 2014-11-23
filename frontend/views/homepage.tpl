<link rel="stylesheet" type="text/css" href="static/demo.css" />

<ul>	
	<li><a href="/">Home</a></li>
	%if signed_in:
		<li>{{email}}</li>
		<li><a href="/signout">Sign Out</a></li>
	%end
	%if not signed_in:
		<li><a href="/login">Sign in</a></li>
	%end
</ul>

<img src="static/logo.png">

<div>
	<form action='/', method="GET">
		Keyword: <input name="keywords" type="text"/>
		<input value="Submit" type="submit"/>
	</form>
</div>
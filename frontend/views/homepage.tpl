<link rel="stylesheet" type="text/css" href="static/css/demo.css" />

<ul>	
	<li><a href="/">Home</a></li>
	%if signed_in:
		<li style="margin-top: 1em">{{email}}</li>
		<li><a href="/signout">Sign Out</a></li>
	%end
	%if not signed_in:
		<li><a href="/login">Sign in</a></li>
	%end
</ul>

<img src="static/images/logo.png">

<div>
	<form action='/', method="GET">
		<input name="keywords" type="text"/>
		<input value="Search" type="submit"/>
	</form>
</div>



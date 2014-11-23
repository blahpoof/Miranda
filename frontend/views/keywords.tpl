<link rel="stylesheet" type="text/css" href="static/demo.css" />

<ul style="list-style-type:none; margin:0; padding:0;">	
	<li><a href="/">Home</a></li>
	%if signed_in:
		<li>{{email}}</li>
		<li><a href="/signout">Sign Out</a></li>
	%end
</ul>

<table style="float: left;" border='1' id="results">
	%if l:
		<caption><b>Results</b></caption>
	%end
	%if not l:
		<caption><b>No Results Found.</b></caption>
	%end
	%for url in l:
		<tr>
			<td>{{url}}</td>
		</tr>
	%end
</table>

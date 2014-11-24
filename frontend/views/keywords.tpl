<link rel="stylesheet" type="text/css" href="static/demo.css" />


<ul style="list-style-type:none; margin:0; padding:0;">	
	<li style=><a href="/">Home</a></li>
	%if signed_in:
		<li>{{email}}</li>
		<li><a href="/signout">Sign Out</a></li>
	%end
</ul>

<div>
	<form action='/', method="GET">
		Keyword: <input name="keywords" type="text"/>
		<input value="Submit" type="submit"/>
	</form>
</div>

<table style="float: left;" border='1' id="results" class="paginated">
	%if not l:
		<b>No Results Found.</b>
	%end
	%if l:
		<thead>
			<tr>
				<th scope="col">Results</th>
			</tr>
		</thead>
	%end	 
	
	<tbody>	
	%for url in l:	
		<tr>
			<td><a href="{{url}}">{{url}}</a></td>
		</tr>
	%end
	</tbody>
</table>

<script src="static/jquery.min.js"></script>
<script src="static/pagination.js"></script>
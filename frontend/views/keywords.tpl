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

<div>
	<form action='/', method="GET">
		<input name="keywords" type="text"/>
		<input value="Search" type="submit"/>
	</form>
</div>

%if not l:
	<li><b>No Results Found.</b></li>
%end

%if corr:
	<li style="margin-top: 1em;">Did you mean <a href="/?keywords={{corr}}">{{corr}}</a>?</li>
%end

<table style="float: left;" border='1' id="results" class="paginated">
	
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
			<td>
				<a href="{{url[0]}}">{{url[1]}}</a>
				<p>{{url[0]}}</p>
			</td>
		</tr>
	%end
	</tbody>
</table>

<script src="static/js/jquery.min.js"></script>
<script src="static/js/pagination.js"></script>
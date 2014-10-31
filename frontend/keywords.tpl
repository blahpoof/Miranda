<ul style="list-style-type:none; margin:0; padding:0;">	
	<li><a href="/">Home</a></li>
	%if signed_in:
		<li>{{email}}</li>
		<li><a href="/signout">Sign Out</a></li>
	%end
</ul>

<table style="float: left;" border='1' id="results">
	%if d:
		<caption><b>Results</b></caption>
	%for key in d:
		<tr>
			<td>{{key}}</td>
			<td>{{d[key]}}</td>
		</tr>
	%end
</table>
%if signed_in:
	<table style="float: left;" border='1' id="history">
		%if l:
			<caption><b>History</b></caption>
		%for word in l:
			<tr>
				<td>{{word[0]}}</td>
				<td>{{word[1]}}</td>
			</tr>
		%end
	</table>
%end
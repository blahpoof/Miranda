<table style="float: left;" border='0' id="results">
	%if d:
		<caption><b>Results</b></caption>
	%for key in d:
		<tr>
			<td>{{key}}</td>
			<td>{{d[key]}}</td>
		</tr>
	%end
</table>
<table style="float: left;" border='0' id="history">
	%if l:
		<caption><b>History</b></caption>
	%for word in l:
		<tr>
			<td>{{word[0]}}</td>
			<td>{{word[1]}}</td>
		</tr>
	%end
</table>
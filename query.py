from bottle import route, run, debug, request, template

history = {}
@route('/', method='GET')
def get_query():
	return '''
		<form action='/results' method="post">
			Keyword: <input name="keywords" type="text"/>
			<input value="Submit" type="submit"/>
		</form>
	'''

@route('/results', method='POST')
def print_query():
	keywords = request.forms.get('keywords')
	if keywords:
		query = {}
		words = keywords.lower().strip().split()
		for word in words:
			history[word] = history.get(word, 0) + 1
			query[word] = query.get(word, 0) + 1
	sorted_history = sorted(history.items(), key=lambda x:x[1], reverse=True )
	return template("keywords", d=query, l=sorted_history[:20])
	
run(host='localhost', port=8080, debug=True, reloader=True)


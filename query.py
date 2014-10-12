from bottle import route, run, debug, request, template

history = {} # Dictionary storing number of times each word has been searched since server start

@route('/', method='GET')
def get_query():
	''' Uses http GET method to get keywords from user via an HTML form. '''

	return '''
		<form action='/results' method="post">
			Keyword: <input name="keywords" type="text"/>
			<input value="Submit" type="submit"/>
		</form>
	''' 

@route('/results', method='POST')
def print_query():
	''' Displays word count of keyword search in an HTML table, and a list of the top 20 most searched words in another HTML table using http POST '''

	keywords = request.forms.get('keywords') # Get keywords from an HTML form 
	if keywords:
		query = {} # Dictionary storing word count of current search
		words = keywords.lower().strip().split() # list of keywords in lowercase form
		for word in words:
			# Add word to dictionaries, or plus one if already in dictionary
			history[word] = history.get(word, 0) + 1
			query[word] = query.get(word, 0) + 1

	sorted_history = sorted(history.items(), key=lambda x:x[1], reverse=True ) # list of (key, value) of history sorted by word count
	return template("keywords", d=query, l=sorted_history[:20]) # Creates tables using HTML template
	
run(host='localhost', port=8080, debug=True, reloader=True)


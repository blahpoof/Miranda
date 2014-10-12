from bottle import route, run, debug, request, template

history = {} # Dictionary storing number of times each word has been searched since server start

@route('/')
def query():
	''' If a keyword string has been searched, returns an HTML table displaying the word count of the string, and another
		HTML table displaying the top 20 most searched words. Otherwise, returns an HTML form requesting a keyword string. '''

	keywords = request.GET.get('keywords', '').strip()

	if keywords: # A keyword string has been submitted
		query = {} # Dictionary storing word count of keywords string 
		words = keywords.lower().strip().split() # list of keywords in lowercase form
		
		for word in words:
			# Add word to dictionaries, or increase count by 1 if already in dictionary
			history[word] = history.get(word, 0) + 1
			query[word] = query.get(word, 0) + 1

		sorted_history = sorted(history.items(), key=lambda x:x[1], reverse=True ) # list of (word, count) of history sorted by count
		return template("keywords", d=query, l=sorted_history[:20]) # display tables using HTML template
	
	else: # A keyword string has not been submitted
		return '''
			<form action='/', method="GET">
				Keyword: <input name="keywords" type="text"/>
				<input value="Submit" type="submit"/>
			</form>
		''' 
	
run(host='localhost', port=8080, debug=True, reloader=True)


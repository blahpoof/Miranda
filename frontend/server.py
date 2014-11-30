from bottle import route, run, debug, request, template, static_file, redirect, response, error
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import sqlite3 as sql
import httplib2
import spell_correct as spell

LOCAL = True

# Classes -------------------------------------------------------
class User(object):
	''' Stores user information and history. '''
	def __init__(self, credentials, email):
		self.credentials = credentials
		self.email = email
		self.history = []

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.email == other.email
		else:
			return False

	def __ne__(self, other):
		return not self.__eq__(other)

# Storage ----------------------------------------------------------
UserList = []

db_conn = sql.connect("dbFile.db")
cur = db_conn.cursor()

# Error Handling ---------------------------------------------------

@error(404)
def error404(error):
	return template("404")

# Static File Serving ----------------------------------------------

@route('/static/images/<filename>')
def server_images(filename):
	return static_file(filename, root='static/images/')

@route('/static/css/<filename>') 
def server_css(filename): 
    return static_file(filename, root='static/css/')

@route('/static/js/<filename>') 
def server_js(filename):
	return static_file(filename, root='static/js/')

@route('/static/fonts/<filename>')
def server_fonts(filename):
	return static_file(filename, root='static/fonts/')

# Query handling -----------------------------------------------------
		
@route('/')
def query_page():
	''' Creates query form and handles query requests. '''
		
	# Check whether user is logged in
	email = request.get_cookie("account", secret='secret_key')
	curr_user = None
	for user in UserList:
		if email == user.email:
			curr_user = user

	# Check if query has been entered
	keywords = request.GET.get('keywords', '').strip()

	if keywords:
		doc_ids = []
		urls = []

		word = keywords.lower().strip().split()[0]

		# Spell correction 
		spellcheck = spell.correct(word) # spellcheck is likely correction of the word, may be identical to word
		if spellcheck == word:
			spellcheck = None

		# Retreive corresponding word_id
		cur.execute('SELECT word_id FROM lexicon WHERE word=?', (word,))
		result = cur.fetchone()

		if result:
			word = result[0]

			# Retreive all doc_ids that have word_id
			for row in cur.execute('SELECT doc_id FROM inverted WHERE word_id=?', (word,)):
				doc_ids.append(row[0])

			# Retreive all search results in pagerank descending order
			for doc_id in doc_ids:
				for row in cur.execute('SELECT url, title FROM documents WHERE doc_id=? ORDER BY pagerank DESC', (doc_id,)):
					url = [row[0].encode('ascii','ignore'), row[1].encode('ascii','ignore')]
					if url not in urls:
						urls.append(url)

			# Don't correct user's input if results are found
			if urls:
				spellcheck = None			

		# Display results page
		if curr_user:
			return template("keywords", signed_in=True, email=curr_user.email, l=urls, corr=spellcheck) # display tables using HTML template
		else:
			return template("keywords", signed_in=False, l=urls, corr=spellcheck)
	
	# Display query form 
	else: 
		if curr_user:
			return template("homepage", signed_in=True, email=curr_user.email, l=curr_user.history, )
		else:
			return template("homepage", signed_in=False)

# Google Login and Logout ------------------------------------------

# oauth2 flow
if LOCAL:
	flow = flow_from_clientsecrets('client_secrets.json',
		scope='https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email',
		redirect_uri="http://localhost:8080/redirect")
else:
	flow = flow_from_clientsecrets('client_secrets.json',
		scope='https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email',
		redirect_uri="http://ec2-54-173-107-230.compute-1.amazonaws.com/redirect")

@route('/login')
def login_page():
	auth_uri = flow.step1_get_authorize_url()
	redirect(str(auth_uri))

@route('/redirect')
def redirect_page():
	''' Handles oauth2 redirect and signs user in. Creates a new User object if that user has not previously signed in before. '''

	# Obtain user code
	code = request.query.get('code', '')
	credentials = flow.step2_exchange(code)

	# Obtain user email
	http=httplib2.Http()
	http = credentials.authorize(http)
	service = build('oauth2', 'v2', http=http);
	document = service.userinfo().get().execute()
	user_email = document['email']

	# Sign in 
	response.set_cookie("account", user_email, secret='secret_key')

	# If user signed in for first time, make new User object
	for user in UserList:
		if user.email == user_email:
			break
	else:
		new_user = User(credentials, user_email)
		UserList.append(new_user)
	
	return redirect('/')

@route('/signout')
def signout_page():
	response.delete_cookie("account", secret='secret_key')
	return redirect('/')


# Deployment -------------------------------------------------

if LOCAL:
	run(host='localhost', port=8080, debug=True, reloader=True)
else:
	run(host='0.0.0.0', port=80, debug=False, reloader=True) 


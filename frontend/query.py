from bottle import route, run, debug, request, template, static_file, redirect, response
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import httplib2

# Classes -----------------------------------------
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

# Storage -----------------------------------------
UserList = []

# Routing -----------------------------------------

# oauth2 flow
flow = flow_from_clientsecrets('client_secrets.json',
		scope='https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email',
		redirect_uri="http://ec2-54-173-107-230.compute-1.amazonaws.com/redirect")
		
@route('/')
def query():
	''' Creates query form and handles query requests based on whether or not user is signed in. '''
		
	# Check whether user is logged in
	email = request.get_cookie("account", secret='secret_key')
	curr_user = None
	for user in UserList:
		if email == user.email:
			curr_user = user

	# Check if query has been entered
	keywords = request.GET.get('keywords', '').strip()

	# Process query results
	if keywords: 
		query = {} 
		words = keywords.lower().strip().split()
		
		for word in words:
			
			# Update results and user history 
			if curr_user:
				if word in curr_user.history:
					curr_user.history.remove(word)
				curr_user.history.append(word)
				while len(curr_user.history) > 10:
					curr_user.history.pop(0)
			query[word] = query.get(word, 0) + 1

		if curr_user:
			return template("keywords", signed_in=True, email=curr_user.email, d=query) # display tables using HTML template
		else:
			return template("keywords", signed_in=False, d=query)
	
	# Display query form 
	else: 
		if curr_user:
			return template("homepage", signed_in=True, email=curr_user.email, l=curr_user.history)
		else:
			return template("homepage", signed_in=False)

@route('/login')
def login():
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
def signout():
	response.delete_cookie("account", secret='secret_key')
	return redirect('/')

@route('/<filename:re:.*\.png>') 
def send_image(filename): 
    return static_file(filename, root='', mimetype='image/png') 

run(host='0.0.0.0', port=80, debug=False, reloader=True)
# run(host='localhost', port=8080, debug=True, reloader=True)


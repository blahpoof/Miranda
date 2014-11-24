from crawler import crawler 
import sqlite3 as lite

#Urls:
# http://duckduckgo.com
# http://google.ca

def tester(d, key, result):
	return d.get(key, None) == result

# Depth 0
db_conn = lite.connect("dbFile.db")
c = crawler(db_conn, "test_urls.txt")
c.crawl( depth = 0 )
db_conn.commit()
db_conn.close()
inverted0 = c.get_inverted_index() 
resolved0 = c.get_resolved_inverted_index() 

# Check whether dictionaries are empty
assert inverted0
assert resolved0

# Check whether non-existent words are in resolved0
assert tester(resolved0, 'fjdkajfldksa', None)
assert tester(resolved0, 'djfkldasjfdja', None)

# Check words known to only be found in a particular url
assert tester(resolved0, 'duckduckgo', set(['http://duckduckgo.com']))
assert tester(resolved0, 'resetthenet', set(['http://duckduckgo.com']))
assert tester(resolved0, 'google', set(['http://google.ca']))
assert tester(resolved0, 'youtube', set(['http://google.ca']))

# Check words known to be found in both urls
assert tester(resolved0, 'about', set(['http://duckduckgo.com', 'http://google.ca']))
assert tester(resolved0, 'search', set(['http://duckduckgo.com', 'http://google.ca']))

# Check for known words are in lexicon
db_conn = lite.connect("dbFile.db")
cur = db_conn.cursor()
cur.execute("SELECT word_id FROM lexicon WHERE word='about'")
about_id = cur.fetchall()
assert len(about_id) > 0
about_id = about_id[0][0]
cur.execute("SELECT word_id FROM lexicon WHERE word='google'")
google_id = cur.fetchall()
assert len(google_id) > 0
google_id = google_id[0][0]

#Check for doc_ids in inverted index
cur.execute("SELECT doc_id FROM inverted WHERE word_id=?", (about_id,))
about_doc_ids = cur.fetchall()
about_doc_ids = list(set(about_doc_ids))
assert len(about_doc_ids) == 2
cur.execute("SELECT doc_id FROM inverted WHERE word_id=?", (google_id,))
google_doc_ids = cur.fetchall()
google_doc_ids = list(set(google_doc_ids))
assert len(google_doc_ids) == 1

#Check for URLs in documents table
for doc_id in about_doc_ids:
	cur.execute("SELECT url FROM documents WHERE doc_id=?", (doc_id[0],))
	assert cur.fetchone()

for doc_id in google_doc_ids:
	cur.execute("SELECT url FROM documents WHERE doc_id=?", (doc_id[0],))
	assert cur.fetchone()

# Depth 1
db_conn = lite.connect("dbFile.db")
c = crawler(db_conn, "test_urls.txt")
c.crawl(depth=1)
inverted1 = c.get_inverted_index()
resolved1 = c.get_resolved_inverted_index()
db_conn.commit()
db_conn.close()

# Check whether dictionaries are empty
assert inverted1
assert resolved1

# Check if there are additional words compared to dictionaries of depth 0 crawler
assert len(inverted1) > len(inverted0)
assert len(resolved1) > len(resolved0)

print "All tests passed"

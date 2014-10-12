from crawler import crawler 

#Urls:
# http://duckduckgo.com
# http://google.ca

def tester(d, key, result):
	return d.get(key, None) == result

# Depth 0
c = crawler(None, "urls.txt")
c.crawl( depth = 0 )
inverted0 = c.get_inverted_index() 
resolved0 = c.get_resolved_inverted_index() 

# Check whether dictionaries are empty
assert inverted0
assert resolved0

# Check whether non-existent words are in resolved0
assert tester(resolved0, u'fjdkajfldksa', None)
assert tester(resolved0, u'djfkldasjfdja', None)

# Check words known to only be found in a particular url
assert tester(resolved0, u'duckduckgo', set(['http://duckduckgo.com']))
assert tester(resolved0, u'resetthenet', set(['http://duckduckgo.com']))
assert tester(resolved0, u'google', set(['http://google.ca']))
assert tester(resolved0, u'youtube', set(['http://google.ca']))

# Check words known to be found in both urls
assert tester(resolved0, u'about', set(['http://duckduckgo.com', 'http://google.ca']))
assert tester(resolved0, u'privacy', set(['http://duckduckgo.com', 'http://google.ca']))

# Depth 1
c = crawler(None, "urls.txt")
c.crawl(depth=1)
inverted1 = c.get_inverted_index()
resolved1 = c.get_resolved_inverted_index()

# Check whether dictionaries are empty
assert inverted1
assert resolved1

# Check if there are additional words compared to dictionaries of depth 0 crawler
assert len(inverted1) > len(inverted0)
assert len(resolved1) > len(resolved0)

print "All tests passed"
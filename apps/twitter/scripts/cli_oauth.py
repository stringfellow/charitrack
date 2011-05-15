import tweepy

CONSUMER_KEY = 'RjojI2CEoi1v8HzhHSj6FQ'
CONSUMER_SECRET = 'yl3NLr8X9xYhMuLC8BB6hf5FL2D6XrWasz4AsLvwzyI'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

x = """auth_url = auth.get_authorization_url()
print 'Please authorize: ' + auth_url
verifier = raw_input('PIN: ').strip()
auth.get_access_token(verifier)
print "ACCESS_KEY = '%s'" % auth.access_token.key
print "ACCESS_SECRET = '%s'" % auth.access_token.secret"""
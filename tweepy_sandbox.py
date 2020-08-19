import dill
import tweepy
import credentials as c

#auth = tweepy.OAuthHandler(c.consumer_key, c.consumer_secret)
#auth.set_access_token(c.access_token, c.access_token_secret)

#api = tweepy.API(auth)
#results = api.search("(#alteryx)", tweet_mode="extended")

with open("parse_test_examples.dill", 'rb') as dill_file:
    tweets = dill.load(dill_file)

print(tweets)


import unittest
import tweepy
import credentials as c
import parsing


class ParseTester(unittest.TestCase):
    def test_parsing_tweet(self):
        auth = tweepy.OAuthHandler(c.consumer_key, c.consumer_secret)
        auth.set_access_token(c.access_token, c.access_token_secret)

        api = tweepy.API(auth)
        results = api.search("(from:tlarsendataguy)", tweet_mode="extended")
        tweet = results[0]
        parsedTweet = parsing.ParsedTweet(tweet)

        self.assertIsNotNone(parsedTweet.Id)



if __name__ == '__main__':
    unittest.main()

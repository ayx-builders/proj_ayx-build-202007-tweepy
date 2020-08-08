import unittest
import parsing
import dill
import tweepy


class ParseTester(unittest.TestCase):
    def test_parsing_tweet(self):
        with open("parse_test_examples.dill", 'rb') as dill_file:
            tweets = dill.load(dill_file)

        for tweet in tweets:
            parsed = parsing.ParsedTweet(tweet)
            self.assertIsNotNone(parsed.Id)


if __name__ == '__main__':
    unittest.main()

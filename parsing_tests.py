import unittest
import parsing
import dill


class ParseTester(unittest.TestCase):
    def test_parsing_tweet(self):
        with open("parse_test_examples.dill", 'rb') as dill_file:
            tweets = dill.load(dill_file)

        index = 0
        for tweet in tweets:
            print(index)
            parsed = parsing.ParsedTweet(tweet)
            self.assertIsNotNone(parsed.Id)
            index += 1


if __name__ == '__main__':
    unittest.main()

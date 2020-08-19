import unittest
import user_input


class UserInputTests(unittest.TestCase):
    def test_keywords(self):
        keyword_input = """"black lives matter" alteryx
alteryx golang
ayx
"""

        twitter_query = user_input.parse_keywords(keyword_input)
        self.assertEqual('(("black lives matter" alteryx) OR (alteryx golang) OR (ayx))', twitter_query)

    def test_mentions(self):
        mentions_input = """tlarsendataguy
@nick612haylund
"""

        twitter_query = user_input.parse_mentions(mentions_input)
        self.assertEqual('(@tlarsendataguy OR @nick612haylund)', twitter_query)

    def test_from(self):
        mentions_input = """tlarsendataguy
@nick612haylund
"""

        twitter_query = user_input.parse_from(mentions_input)
        self.assertEqual('(from:@tlarsendataguy OR from:@nick612haylund)', twitter_query)

    def test_to(self):
        mentions_input = """tlarsendataguy
@nick612haylund
"""

        twitter_query = user_input.parse_to(mentions_input)
        self.assertEqual('(to:@tlarsendataguy OR to:@nick612haylund)', twitter_query)

    def test_from_to(self):
        mentions_input = """tlarsendataguy
@nick612haylund
"""

        twitter_query = user_input.parse_from_to(mentions_input)
        self.assertEqual('(from:@tlarsendataguy OR from:@nick612haylund OR to:@tlarsendataguy OR to:@nick612haylund)', twitter_query)

    def test_hashtags(self):
        mentions_input = """tlarsendataguy
#nick612haylund
"""

        twitter_query = user_input.parse_hashtags(mentions_input)
        self.assertEqual('(#tlarsendataguy OR #nick612haylund)', twitter_query)

    def test_empty(self):
        twitter_query = user_input.parse_keywords("")
        self.assertEqual('', twitter_query)


if __name__ == '__main__':
    unittest.main()

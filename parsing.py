from datetime import datetime

Fields = {
    'Id': 'string',
    'CreatedAt': 'datetime',
    'Text': 'string',
    'Source': 'string',
    'UserId': 'string',
    'ScreenName': 'string',
    'UserLocation': 'string',
    'UserDescription': 'string',
    'UserVerified': 'bool',
    'UserFollowers': 'int',
    'UserFriends': 'int',
    'UserFavorites': 'int',
    'UserTweets': 'int',
    'UserCreatedAt': 'datetime',
    'RetweetCount': 'int',
    'FavoriteCount': 'int',
    'PossiblySensitive': 'bool',
    'Language': 'string',
    'TweetType': 'string',


    # these fields are not often used so we will exclude them for now.  Can be added back later
    #'Lon': 'decimal',
    #'Lat': 'decimal',
    #'PlaceType': 'string',
    #'PlaceName': 'string',
    #'PlaceFullName': 'string',
    #'PlaceCountryCode': 'string',
    #'PlaceCountry': 'string',
    #'PlaceCentroidLat': 'decimal',
    #'PlaceCentroidLon': 'decimal',
}


class ReplyTweet:
    def __init__(self, id, user_id, user_screen_name):
        self.Id: id
        self.CreatedAt = None
        self.Text = None
        self.Source = None
        self.UserId = user_id
        self.ScreenName = user_screen_name
        self.UserLocation = None
        self.UserDescription = None
        self.UserVerified = None
        self.UserFollowers = None
        self.UserFriends = None
        self.UserFavorites = None
        self.UserTweets = None
        self.UserCreatedAt = None
        self.RetweetCount = None
        self.FavoriteCount = None
        self.PossiblySensitive = None
        self.Language = None


class ParsedTweet:
    def __init__(self, tweet, recurse=True):
        self.Id: str = tweet.id_str
        self.CreatedAt: datetime = tweet.created_at
        self.Text: str = tweet.full_text
        self.Source: str = tweet.source
        self.UserId: str = tweet.user.id_str
        self.ScreenName: str = tweet.user.screen_name
        self.UserLocation: str = tweet.user.location
        self.UserDescription: str = tweet.user.description
        self.UserVerified: bool = tweet.user.verified
        self.UserFollowers: int = tweet.user.followers_count
        self.UserFriends: int = tweet.user.friends_count
        self.UserFavorites: int = tweet.user.favourites_count
        self.UserTweets: int = tweet.user.statuses_count
        self.UserCreatedAt: datetime = tweet.user.created_at
        self.RetweetCount: int = tweet.retweet_count
        self.FavoriteCount: int = tweet.favorite_count
        if hasattr(tweet, 'possibly_sensitive'):
            self.PossiblySensitive: bool = tweet.possibly_sensitive
        else:
            self.PossiblySensitive = None
        self.Language: str = tweet.lang

        if not recurse:
            return

        self.TweetType = "Tweet"
        self.OriginalTweet = None
        if hasattr(tweet, 'retweeted_status'):
            self.TweetType = "Retweet"
            self.OriginalTweet = ParsedTweet(tweet.retweeted_status, recurse=False)
            self.Text = None
            return
        if tweet.is_quote_status:
            self.TweetType = "Retweet with Comment"
            self.OriginalTweet = ParsedTweet(tweet.quoted_status, recurse=False)
            return
        if tweet.in_reply_to_status_id_str is not None:
            self.TweetType = "Reply"
            id = tweet.in_reply_to_status_id_str
            user_id = tweet.in_reply_to_user_id_str
            screen_name = tweet.in_reply_to_screen_name
            self.OriginalTweet = ReplyTweet(id, user_id, screen_name)

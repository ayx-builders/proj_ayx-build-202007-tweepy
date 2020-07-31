from datetime import datetime

Fields = {
    'Id': 'string',
    'CreatedAt': 'datetime',
    'Text': 'string',
    'Source': 'string',
    'InReplyToTweet': 'string',
    'InReplyToUser': 'string',
    'InReplyToScreenName': 'string',
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
    'Lon': 'decimal',
    'Lat': 'decimal',
    'PlaceType': 'string',
    'PlaceName': 'string',
    'PlaceFullName': 'string',
    'PlaceCountryCode': 'string',
    'PlaceCountry': 'string',
    'PlaceCentroidLat': 'decimal',
    'PlaceCentroidLon': 'decimal',
    'RetweetId': 'string',
    'IsRetweet': 'bool',
    'RetweetCount': 'int',
    'FavoriteCount': 'int',
    'PossiblySensitive': 'bool',
    'Language': 'string'
}

class ParsedTweet:
    def __init__(self, tweet):
        self.Id: str = tweet.id_str
        self.CreatedAt: datetime = tweet.created_at
        self.Text: str = tweet.full_text
        self.Source: str = tweet.source
        self.InReplyToTweet: str = tweet.in_reply_to_status_id_str
        self.InReplyToUser: str = tweet.in_reply_to_user_id_str
        self.InReplyToScreenName: str = tweet.in_reply_to_screen_name
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
        coords = tweet.coordinates
        if coords is not None:
            self.Lon: float = coords.coordinates[0]
            self.Lat: float = coords.coordinates[1]
        else:
            self.Lat = None
            self.Lon = None
        place = tweet.place
        if place is not None:
            self.PlaceType: str = place.place_type
            self.PlaceName: str = place.name
            self.PlaceFullName: str = place.full_name
            self.PlaceCountryCode: str = place.country_code
            self.PlaceCountry: str = place.country
            if hasattr(place, 'coordinates'):
                coordinates = place.coordinates
                coord1 = coordinates[0][0]
                coord2 = coordinates[0][2]
                lat = (coord1[0] + coord2[0]) / 2
                lon = (coord1[1] + coord2[1]) / 2
                self.PlaceCentroidLat = lat
                self.PlaceCentroidLon = lon
            else:
                self.PlaceCentroidLat = None
                self.PlaceCentroidLon = None
        else:
            self.PlaceType = None
            self.PlaceName = None
            self.PlaceFullName = None
            self.PlaceCountryCode = None
            self.PlaceCountry = None
            self.PlaceCentroidLat = None
            self.PlaceCentroidLon = None
        if hasattr(tweet, 'retweeted_status'):
            originalTweet = tweet.retweeted_status
            self.RetweetId: str = originalTweet.id_str
            self.IsRetweet: bool = True
        else:
            self.RetweetId = None
            self.IsRetweet = False
        self.RetweetCount: int = tweet.retweet_count
        self.FavoriteCount: int = tweet.favorite_count
        if hasattr(tweet, 'possibly_sensitive'):
            self.PossiblySensitive: bool = tweet.possibly_sensitive
        else:
            self.PossiblySensitive = None
        self.Language: str = tweet.lang

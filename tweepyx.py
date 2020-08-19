import datetime
import AlteryxPythonSDK as Sdk
import xml.etree.ElementTree as Et
import tweepy
import user_input
from obj_query import AyxDataMap, FieldType, Query


def none_to_empty_string(value):
    if value is None:
        return ''
    else:
        return value


def get_text_from_xml(value):
    if value is None:
        return None
    else:
        return value.text


class AyxPlugin:
    def __init__(self, n_tool_id: int, alteryx_engine: object, output_anchor_mgr: object):
        # Default properties
        self.n_tool_id: int = n_tool_id
        self.alteryx_engine: Sdk.AlteryxEngine = alteryx_engine
        self.output_anchor_mgr: Sdk.OutputAnchorManager = output_anchor_mgr
        self.label = "Tweepyx (" + str(n_tool_id) + ")"

        # Custom properties
        self.Query: str = ''
        self.ConsumerKey: str = ''
        self.ConsumerSecret: str = ''
        self.AccessToken: str = ''
        self.AccessSecret: str = ''

    def pi_init(self, str_xml: str):
        xml_parser = Et.fromstring(str_xml)

        self.ConsumerKey = get_text_from_xml(xml_parser.find('ConsumerKey'))
        self.ConsumerSecret = get_text_from_xml(xml_parser.find('ConsumerSecret'))
        self.AccessToken = get_text_from_xml(xml_parser.find('AccessToken'))
        self.AccessSecret = get_text_from_xml(xml_parser.find('AccessSecret'))

        if self.ConsumerKey is None or self.ConsumerSecret is None or self.AccessToken is None or self.AccessSecret is None:
            self.display_error_msg(
                "All credentials must be provided.  You can find your credentials at developer.twitter.com")

        from_date = xml_parser.find('From').text
        to_date = datetime.datetime.strptime(xml_parser.find('To').text, "%Y-%m-%d") + datetime.timedelta(days=1)
        language = xml_parser.find('Language').text
        exclude_retweets = xml_parser.find("ExcludeRetweets").text == 'True'
        keywords = user_input.parse_keywords(none_to_empty_string(xml_parser.find('Keywords').text))
        mentions = user_input.parse_mentions(none_to_empty_string(xml_parser.find('Mentions').text))
        hashtags = user_input.parse_hashtags(none_to_empty_string(xml_parser.find('Hashtags').text))

        query_elements = []
        if keywords != '':
            query_elements.append(keywords)
        if mentions != '':
            query_elements.append(mentions)
        if hashtags != '':
            query_elements.append(hashtags)
        if language != 'All':
            query_elements.append("lang:" + language)
        if exclude_retweets:
            query_elements.append("-filter:retweets")

        if len(query_elements) == 0:
            self.display_error_msg("At least one of keywords, mentions, or hashtags must be provided.")

        query_elements.append("since:" + from_date)
        query_elements.append("until:" + datetime.datetime.strftime(to_date, "%Y-%m-%d"))
        self.Query = " AND ".join(query_elements)

        # Getting the output anchor from Config.xml by the output connection name
        self.Output = self.output_anchor_mgr.get_output_anchor('Output')

    def pi_add_incoming_connection(self, str_type: str, str_name: str) -> object:
        raise Exception('not implemented')

    def pi_add_outgoing_connection(self, str_name: str) -> bool:
        return True

    def pi_push_all_records(self, n_record_limit: int) -> bool:
        def orig_tweet():
            return Query().custom(get_original_tweet)
        data_mapper = AyxDataMap(self.alteryx_engine, self.label, {
            ('Id', FieldType.String): Query().get('id_str').finalize(),
            ('TweetType', FieldType.String): Query().custom(get_tweet_type).finalize(),
            ('CreatedAt', FieldType.Datetime): Query().get('created_at').finalize(),
            ('Text', FieldType.String): Query().custom(get_full_text).finalize(),
            ('Source', FieldType.String): Query().get('source').finalize(),
            ('UserId', FieldType.String): Query().get('user').get('id_str').finalize(),
            ('ScreenName', FieldType.String): Query().get('user').get('screen_name').finalize(),
            ('UserLocation', FieldType.String): Query().get('user').get('location').finalize(),
            ('UserDescription', FieldType.String): Query().get('user').get('description').finalize(),
            ('UserVerified', FieldType.Bool): Query().get('user').get('verified').finalize(),
            ('UserFollowers', FieldType.Integer): Query().get('user').get('followers_count').finalize(),
            ('UserFriends', FieldType.Integer): Query().get('user').get('friends_count').finalize(),
            ('UserFavorites', FieldType.Integer): Query().get('user').get('favourites_count').finalize(),
            ('UserTweets', FieldType.Integer): Query().get('user').get('statuses_count').finalize(),
            ('UserCreatedAt', FieldType.Datetime): Query().get('user').get('created_at').finalize(),
            ('RetweetCount', FieldType.Integer): Query().get('retweet_count').finalize(),
            ('FavoriteCount', FieldType.Integer): Query().get('favorite_count').finalize(),
            ('PossiblySensitive', FieldType.Bool): Query().get('possibly_sensitive').finalize(),
            ('Language', FieldType.String): Query().get('lang').finalize(),
            ('Url', FieldType.String): Query().custom(tweet_url).finalize(),
            ('OriginalTweetId', FieldType.String): orig_tweet().get('id_str').finalize(),
            ('OriginalTweetCreatedAt', FieldType.Datetime): orig_tweet().get('created_at').finalize(),
            ('OriginalTweetText', FieldType.String): orig_tweet().custom(get_full_text).finalize(),
            ('OriginalTweetSource', FieldType.String): orig_tweet().get('source').finalize(),
            ('OriginalTweetUserId', FieldType.String): orig_tweet().get('user').get('id_str').finalize(),
            ('OriginalTweetScreenName', FieldType.String): orig_tweet().get('user').get('screen_name').finalize(),
            ('OriginalTweetUserLocation', FieldType.String): orig_tweet().get('user').get('location').finalize(),
            ('OriginalTweetUserDescription', FieldType.String): orig_tweet().get('user').get('description').finalize(),
            ('OriginalTweetUserVerified', FieldType.Bool): orig_tweet().get('verified').finalize(),
            ('OriginalTweetUserFollowers', FieldType.Integer): orig_tweet().get('user').get('followers_count').finalize(),
            ('OriginalTweetUserFriends', FieldType.Integer): orig_tweet().get('user').get('friends_count').finalize(),
            ('OriginalTweetUserFavorites', FieldType.Integer): orig_tweet().get('user').get('favourites_count').finalize(),
            ('OriginalTweetUserTweets', FieldType.Integer): orig_tweet().get('user').get('statuses_count').finalize(),
            ('OriginalTweetUserCreatedAt', FieldType.Datetime): orig_tweet().get('user').get('created_at').finalize(),
            ('OriginalTweetRetweetCount', FieldType.Integer): orig_tweet().get('retweet_count').finalize(),
            ('OriginalTweetFavoriteCount', FieldType.Integer): orig_tweet().get('favorite_count').finalize(),
            ('OriginalTweetPossiblySensitive', FieldType.Bool): orig_tweet().get('possibly_sensitive').finalize(),
            ('OriginalTweetLanguage', FieldType.String): orig_tweet().get('lang').finalize(),
            ('OriginalTweetUrl', FieldType.String): orig_tweet().custom(tweet_url).finalize(),
        })
        self.Output.init(data_mapper.Info)

        if self.alteryx_engine.get_init_var(self.n_tool_id, "UpdateOnly") == "True":
            self.Output.close()
            return True

        consumer_key = self.alteryx_engine.decrypt_password(self.ConsumerKey)
        consumer_secret = self.alteryx_engine.decrypt_password(self.ConsumerSecret)
        access_token = self.alteryx_engine.decrypt_password(self.AccessToken)
        access_secret = self.alteryx_engine.decrypt_password(self.AccessSecret)

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)

        api = tweepy.API(auth, wait_on_rate_limit=True)

        for raw_tweet in tweepy.Cursor(api.search, q=self.Query, tweet_mode="extended").items():
            blob = data_mapper.transfer(raw_tweet)
            self.Output.push_record(blob)

        self.Output.close()
        return True

    def pi_close(self, b_has_errors: bool):
        return

    def display_error_msg(self, msg_string: str):
        self.alteryx_engine.output_message(self.n_tool_id, Sdk.EngineMessageType.error, msg_string)

    def display_info_msg(self, msg_string: str):
        self.alteryx_engine.output_message(self.n_tool_id, Sdk.EngineMessageType.info, msg_string)

    def ii_close(self):
        self.Output.assert_close()
        return


def get_tweet_type(obj):
    retweeted_status = Query().get('retweeted_status').finalize().get_from(obj)
    is_quote_status = Query().get('is_quote_status').finalize().get_from(obj)
    in_reply_to_status_id = Query().get('in_reply_to_status_id_str').finalize().get_from(obj)
    if retweeted_status is not None:
        return 'Retweet'
    if is_quote_status is not None and is_quote_status is True:
        return 'Retweet with Comment'
    if in_reply_to_status_id is not None:
        return 'Reply'
    return 'Tweet'


def get_full_text(obj):
    retweeted_status = Query().get('retweeted_status').finalize().get_from(obj)
    if retweeted_status is not None:
        return None
    return Query().get('full_text').finalize().get_from(obj)


def get_original_tweet(obj):
    retweeted_status = Query().get('retweeted_status').finalize().get_from(obj)
    if retweeted_status is not None:
        return retweeted_status

    quoted_status = Query().get('quoted_status').finalize().get_from(obj)
    if quoted_status is not None:
        return quoted_status

    reply_id = Query().get('in_reply_to_status_id_str').finalize().get_from(obj)
    reply_user_id = Query().get('in_reply_to_status_user_id_str').finalize().get_from(obj)
    reply_screen_name = Query().get('in_reply_to_status_screen_name').finalize().get_from(obj)
    return {
        "id_str": reply_id,
        "user": {
            "id_str": reply_user_id,
            "screen_name": reply_screen_name,
        }
    }


def tweet_url(obj):
    screen_name = Query().get('user').get('screen_name').finalize().get_from(obj)
    tweet_id = Query().get('id_str').finalize().get_from(obj)
    if screen_name is None or tweet_id is None:
        return None
    return "https://twitter.com/" + screen_name + "/status/" + tweet_id

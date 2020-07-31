import datetime

import AlteryxPythonSDK as Sdk
import xml.etree.ElementTree as Et
import tweepy

import parsing
import user_input


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
        to_date = xml_parser.find('To').text
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

        if len(query_elements) == 0:
            self.display_error_msg("At least one of keywords, mentions, or hashtags must be provided.")

        query_elements.append("since:" + from_date)
        query_elements.append("until:" + to_date)
        self.Query = " AND ".join(query_elements)

        # Getting the output anchor from Config.xml by the output connection name
        self.Output = self.output_anchor_mgr.get_output_anchor('Output')

    def pi_add_incoming_connection(self, str_type: str, str_name: str) -> object:
        raise Exception('not implemented')

    def pi_add_outgoing_connection(self, str_name: str) -> bool:
        return True

    def pi_push_all_records(self, n_record_limit: int) -> bool:
        info = self.createRecordInfo()
        self.Output.init(info)

        if self.alteryx_engine.get_init_var(self.n_tool_id, "UpdateOnly") == "True":
            self.Output.close()
            return True

        creator: Sdk.RecordCreator = info.construct_record_creator()

        consumer_key = self.alteryx_engine.decrypt_password(self.ConsumerKey)
        consumer_secret = self.alteryx_engine.decrypt_password(self.ConsumerSecret)
        access_token = self.alteryx_engine.decrypt_password(self.AccessToken)
        access_secret = self.alteryx_engine.decrypt_password(self.AccessSecret)

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)

        api = tweepy.API(auth)

        for raw_tweet in tweepy.Cursor(api.search, q=self.Query, tweet_mode="extended").items():
            creator.reset()
            tweet = parsing.ParsedTweet(raw_tweet)
            for key in parsing.Fields:
                self.display_info_msg(key)
                value = getattr(tweet, key)
                field: Sdk.Field = info.get_field_by_name(key)
                if value is None:
                    field.set_null(creator)
                    continue

                field_type = parsing.Fields[key]
                if field_type == 'string':
                    field.set_from_string(creator, value)
                if field_type == 'datetime':
                    field.set_from_string(creator, value.strftime("%Y-%m-%d"))
                if field_type == 'int':
                    field.set_from_int64(creator, value)
                if field_type == 'decimal':
                    field.set_from_double(creator, value)
                if field_type == 'bool':
                    field.set_from_bool(creator, value)

            blob = creator.finalize_record()
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

    def createRecordInfo(self):
        info = Sdk.RecordInfo(self.alteryx_engine)
        for key in parsing.Fields:
            fieldType = parsing.Fields[key]
            if fieldType == 'string':
                info.add_field(key, Sdk.FieldType.v_wstring, size=512, source=self.label)
            if fieldType == 'datetime':
                info.add_field(key, Sdk.FieldType.datetime, source=self.label)
            if fieldType == 'int':
                info.add_field(key, Sdk.FieldType.int64, source=self.label)
            if fieldType == 'decimal':
                info.add_field(key, Sdk.FieldType.double, source=self.label)
            if fieldType == 'bool':
                info.add_field(key, Sdk.FieldType.bool, source=self.label)
        return info

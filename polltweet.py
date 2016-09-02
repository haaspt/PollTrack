from __future__ import print_function
import twitter
import logging
import traceback

class PollTweet(object):

    def __init__(self, user_consumer_key, user_consumer_secret, user_access_token_key, user_access_token_secret):
        self.twitter = twitter.Api(consumer_key = user_consumer_key,
                                   consumer_secret = user_consumer_secret,
                                   access_token_key = user_access_token_key,
                                   access_token_secret = user_access_token_secret)

    def tweet_poll(self, poll_data):
        # Parse out poll_data
        self.twitter.PostUpdate(poll_data)

    def tweet_polls(self, poll_dataframe):
        for poll_data in poll_dataframe:
            self.tweet_poll(poll_data)

    def tweet_average(self, average_data):
        # Do something
        self.twitter.PostMedia(average_data, average_img)

    def get_mentions(self):
        mentions = [mention for mention in self.twitter.GetMentions]
        return mentions

    def reply_to_mention(self, mention):
        # Parse mention syntax
        return

    
        

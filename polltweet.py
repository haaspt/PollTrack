from __future__ import print_function
import twitter

class PollTweet(object):

    def __init__(self, consumer_key, consumer_secret, access_token_key, access_token_secret):
        self.twitter = twitter.api(consumer_key = consumer_key,
                                   consumer_secret = consumer_secret,
                                   access_token_key = access_token_key,
                                   access_token_secret)

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

    
        

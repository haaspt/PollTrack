from __future__ import print_function
import twitter
import logging
import traceback


logger = logging.getLogger(__name__)

class Tweet(object):


    def __init__(self, pollster, start_date, end_date, clinton_pct, trump_pct,
                 other_pct=None, undecided_pct=None, johnson_pct=None, stein_pct=None):
        self.pollster = pollster
        self.start_date = start_date
        self.end_date = end_date
        self.clinton_pct = clinton_pct
        self.trump_pct = trump_pct
        self.other_pct = other_pct
        self.undecided_pct = undecided_pct
        self.johnson_pct = johnson_pct
        self.stein_pct = stein_pct

    def __repr__(self):
        return """
        Pollster: {pollster}
        Start Date: {start_date}
        End Date: {end_date}
        Clinton: {clinton_pct}
        Trump: {trump_pct}
        Other: {other_pct}
        Undecided: {undecided_pct}
        Johnson: {johnson_pct}
        Stein: {stein_pct}
        """.format(pollster = self.pollster, start_date = self.start_date,
                   end_date = self.end_date, clinton_pct = self.clinton_pct,
                   trump_pct = self.trump_pct, other_pct = self.other_pct,
                   undecided_pct = self.undecided_pct, johnson_pct = self.johnson_pct,
                   stein_pct = self.stein_pct)


class PollTweet(object):

    def __init__(self, user_consumer_key, user_consumer_secret, user_access_token_key, user_access_token_secret):
        self.twitter = twitter.Api(consumer_key = user_consumer_key,
                                   consumer_secret = user_consumer_secret,
                                   access_token_key = user_access_token_key,
                                   access_token_secret = user_access_token_secret)

    def pandas_to_tweet(self, dataframe):
        if dataframe is None:
            #This is, strickly speaking, uncessecary
            return None
        else:
            tweet_list = []
            for row in new_polls.iterrows():
                row = row[1]
                tweet = Tweet(row['Pollster'], row['Start Date'], row['End Date'],
                              row['Clinton'], row['Trump'], row['Other'], row['Undecided'])
                tweet_list.append(tweet)
            return tweet_list

    def tweet_poll(self, tweet):
        # Parse out poll_data
        self.twitter.PostUpdate(tweet)

    def tweet_polls(self, list_of_tweets):
        for tweet in list_of_tweets:
            self.tweet_poll(tweet)

    def tweet_average(self, average_data):
        # Do something
        self.twitter.PostMedia(average_data, average_img)

    def get_mentions(self):
        mentions = [mention for mention in self.twitter.GetMentions]
        return mentions

    def reply_to_mention(self, mention):
        # Parse mention syntax
        return

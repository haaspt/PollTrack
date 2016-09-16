import twitter
import logging
import traceback

logger = logging.getLogger(__name__)

class TweetError(Exception):
    pass


class Tweet(object):

    def __init__(self, pollster, observations, population, start_date, end_date, clinton_pct, trump_pct, other_pct=None, undecided_pct=None, johnson_pct=None, stein_pct=None):
        self.pollster = pollster
        self.observations = int(observations)
        self.population = population
        self.start_date = start_date
        self.end_date = end_date
        self.clinton_pct = clinton_pct
        self.trump_pct = trump_pct
        self.other_pct = other_pct
        self.undecided_pct = undecided_pct
        self.johnson_pct = johnson_pct
        self.stein_pct = stein_pct

        self.long_tweet = "#Clinton: {clinton_pct}\n#Trump: {trump_pct}\nOther: {other_pct}\nUndecided: {undecided_pct}\n\n{pollster} ({start_date} - {end_date})\n{population}".format(clinton_pct=self.clinton_pct,
                                                                                                                                                                                        trump_pct = self.trump_pct,
                                                                                                                                                                                        other_pct=self.other_pct,
                                                                                                                                                                                        undecided_pct=self.undecided_pct,
                                                                                                                                                                                        pollster=self.pollster,
                                                                                                                                                                                        start_date=self.start_date,
                                                                                                                                                                                        end_date=self.end_date,
                                                                                                                                                                                        population = self.population)
        
        self.short_tweet = "C: {clinton_pct}\nT: {trump_pct}\n\n{pollster} ({start_date} - {end_date})\n{population}".format(clinton_pct = self.clinton_pct,
                                                                                                               trump_pct = self.trump_pct,
                                                                                                               pollster = self.pollster,
                                                                                                               start_date = self.start_date,
                                                                                                                             end_date = self.end_date,
        population = self.population)

    def get_tweetable_poll(self):
        """Checks whether the long or short form of a tweet is under the character limit.

        Returns
        -------
        String less than or equal to the Twitter character limit, or None
        """
        if len(self.long_tweet) <= 140: #Check actual character length requirements
            return self.long_tweet
        elif len(self.short_tweet) <= 140:
            return self.short_tweet
        else:
            return None
        
    def __repr__(self):
        return """
        Pollster: {pollster}
        Observations: {observations}
        Population: {population}
        Start Date: {start_date}
        End Date: {end_date}
        Clinton: {clinton_pct}
        Trump: {trump_pct}
        Other: {other_pct}
        Undecided: {undecided_pct}
        Johnson: {johnson_pct}
        Stein: {stein_pct}
        """.format(pollster = self.pollster,
                   observations = self.observations,
                   population = self.population,
                   start_date = self.start_date,
                   end_date = self.end_date,
                   clinton_pct = self.clinton_pct,
                   trump_pct = self.trump_pct,
                   other_pct = self.other_pct,
                   undecided_pct = self.undecided_pct,
                   johnson_pct = self.johnson_pct,
                   stein_pct = self.stein_pct)

    def __str__(self):
        return self.long_tweet
    
    def __len__(self):
        return {"long": len(self.long_tweet), "short": len(self.short_tweet)}


class PollTweet(object):

    def __init__(self, user_consumer_key, user_consumer_secret, user_access_token_key, user_access_token_secret):
        self.twitter = twitter.Api(consumer_key = user_consumer_key,
                                   consumer_secret = user_consumer_secret,
                                   access_token_key = user_access_token_key,
                                   access_token_secret = user_access_token_secret)

    def pandas_to_tweet(self, dataframe):
        """Converts a pandas dataframe to a list of Tweet objects

        Parameters
        ----------
        dataframe: pandas dataframe

        Returns
        -------
        List of Tweet objects
        """
        if dataframe is None:
            return None
        else:
            tweet_list = []
            for row in dataframe.iterrows():
                row = row[1]
                tweet = Tweet(row['Pollster'],
                              row['Number of Observations'],
                              row['Population'],
                              row['Start Date'].strftime('%b %d'), #Short date (e.g. Jun 26)
                              row['End Date'].strftime('%b %d'),
                              row['Clinton'],
                              row['Trump'],
                              row['Other'],
                              row['Undecided'])
                tweet_list.append(tweet)
            return tweet_list

    def tweet_poll(self, tweet):
        """Posts a single poll to Twitter

        Parameters
        ----------
        tweet: Tweet (object)

        """
        if not isinstance(tweet, Tweet):
            raise TweetError("Object passed is not a Tweet object. Unable to post")
        else:
            tweet_to_post = tweet.get_tweetable_poll()
            if tweet_to_post is not None:
                logger.info("Tweeting poll")
                try:
                    self.twitter.PostUpdate(tweet_to_post, verify_status_length=False) #Currently throws a legth exception unless this is set to false. Not sure why
                except Exception as error:
                    logger.error(traceback.format_exc())
            else:
                logger.error("Could not tweet poll. Max characters exceeded")
                logger.error(tweet)

    def tweet_polls(self, list_of_tweets):
        """Iterates through a list of tweets and passes each to self.tweet_poll()

        Parameters
        ----------
        list_of_tweets: list (of Tweet objects)
        """
        logger.info("Tweeting %d new polls", len(list_of_tweets))
        for tweet in list_of_tweets:
            try:
                self.tweet_poll(tweet)
            except TweetError as error:
                logger.error(traceback.format_exc())


    def tweet_average(self, average_data):
        # Do something
        self.twitter.PostMedia(average_data, average_img)

    def get_mentions(self):
        mentions = [mention for mention in self.twitter.GetMentions]
        return mentions

    def reply_to_mention(self, mention):
        # Parse mention syntax
        return

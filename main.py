#!/usr/bin/env python
from __future__ import print_function
from pollio import PollIO
from polltweet import PollTweet
from pollparse import PollParse
import os.path
import json
import logging

logger = logging.getLogger(__name__)

class ConfigFileError(Exception):
    pass

def get_and_tweet_new_polls(url, polltweet_instance):
    """Calls PollIO to check for new polls and tweets any it finds

    Parameters
    ----------
    url: string
        The url to the poll csv on HuffPoPollster

    polltweet_instance: PollTweet (object)
        Instance of the PollTweet object
    """
    logger.debug("Attempting to get new polls")
    pollio = PollIO(url, "./data/", "data.csv")
    if pollio.new_poll_data is not None:
        logger.debug("Attempting to tweet new polls")
        tweet_list = polltweet_instance.pandas_to_tweet(pollio.new_poll_data)
        polltweet_instance.tweet_polls(tweet_list)
        
def main():

    logger.info("PollTrack starting. Loading credentials")
    if not os.path.isfile('credentials.config'):
        logger.error("Credentials file not found")
        raise CongigFileError("Credentials file not found, please see documentation for created a credential file")
    else:
        with open('credentials.config') as file:
            credentials = json.load(file)
            twitter_credentials = credentials['twitter_credentials']
            file.close()
            logger.debug("Credentials loaded")

    polltweet = PollTweet(twitter_credentials['consumer_key'],
                          twitter_credentials['consumer_secret'],
                          twitter_credentials['access_token_key'],
                          twitter_credentials['access_token_secret'])

    poll_url = "http://elections.huffingtonpost.com/pollster/2016-general-election-trump-vs-clinton.csv"

    logger.info("Entering main loop")
    while True:
        get_and_tweet_new_polls(poll_url, polltweet)

if __name__ == "__main__":
    main()

#!/usr/bin/env python
from __future__ import print_function
from pollio import PollIO
from polltweet import PollTweet
from pollparse import PollParse
import os.path
import json
import logging
import time

class ConfigFileError(Exception):
    pass

def get_and_tweet_new_polls(state, url, polltweet_instance):
    """Calls PollIO to check for new polls and tweets any it finds

    Parameters
    ----------
    state: string
        The state (or general scope) of the poll being passed

    url: string
        The url to the poll csv on HuffPoPollster

    polltweet_instance: PollTweet (object)
        Instance of the PollTweet object
    """
    logger.debug("Attempting to get new polls")
    pollio = PollIO(state,
                    url,
                    "./data/",
                    "{0}_data.csv".format(state).lower.replace(" ", "_")
                    
    if pollio.new_poll_data is not None:
        logger.debug("Attempting to tweet new polls")
        tweet_list = polltweet_instance.pandas_to_tweet(pollio.new_poll_data)
        polltweet_instance.tweet_polls(tweet_list)
        pollio.save_poll_data()
        
def main():

    logger.info("PollTrack starting. Loading credentials")
    if not os.path.isfile('credentials.config'):
        logger.error("Credentials file not found")
        raise CongigFileError("Credentials file not found, please see documentation for created a credential file")
    else:
        with open('./credentials.config') as file:
            credentials = json.load(file)
            twitter_credentials = credentials['twitter_credentials']
            file.close()
            logger.debug("Credentials loaded")

    logger.info("Loading poll list")
    if not os.path.isfile('polls.json'):
        logger.error("Poll list file not found")
        raise ConfigFileError("Poll list file not found, please re-install or restore polls.json")
    else:
        with open('./polls.json') as file:
            poll_file = json.load(file)
            poll_url_list = poll_file['poll_list']
            file.close()
            logger.debug("Poll list loaded")
            
    polltweet = PollTweet(twitter_credentials['consumer_key'],
                          twitter_credentials['consumer_secret'],
                          twitter_credentials['access_token_key'],
                          twitter_credentials['access_token_secret'])

#    poll_url = "http://elections.huffingtonpost.com/pollster/2016-general-election-trump-vs-clinton.csv" #Replace with loop through poll_url_list

    logger.info("Entering main loop")
    while True:
        for state, poll_url in poll_url_list.items():
            get_and_tweet_new_polls(state, poll_url, polltweet)
        logger.debug("Sleeping for 10 mins...")
        time.sleep(600)
        
if __name__ == "__main__":
    logging.basicConfig(filename='applog.log',
                        format='%(asctime)s-%(name)s :: %(levelname)s :: %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)
    main()

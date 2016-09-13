#!/usr/bin/env python
from __future__ import print_function
from pollio import PollIO
from polltweet import PollTweet
from pollparse import PollParse
import os.path
import json
import logging

class ConfigFileError(Exception):
    pass

def get_and_tweet_new_polls(url, polltweet_instance):

    pollio = PollIO(url, "./data/", "data.csv")
    if pollio.new_poll_data is not None:
        tweet_list = polltweet_instance.pandas_to_tweet(pollio.new_poll_data)
        polltweet_instance.tweet_polls(tweet_list)

def main():

    if not os.path.isfile('credentials.config'):
        raise CongigFileError("Credentials file not found, please see documentation for created a credential file")
    else:
        with open('credentials.config') as file:
            credentials = json.load(file)
            twitter_credentials = credentials['twitter_credentials']
            file.close()

    polltweet = PollTweet(twitter_credentials['consumer_key'],
                          twitter_credentials['consumer_secret'],
                          twitter_credentials['access_token_key'],
                          twitter_credentials['access_token_secret'])

    poll_url = "http://elections.huffingtonpost.com/pollster/2016-general-election-trump-vs-clinton.csv"

    while True:
        get_and_tweet_new_polls(poll_url, polltweet)

if __name__ == "__main__":
    main()

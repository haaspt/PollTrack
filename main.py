from __future__ import print_function
from pollio import PollIO
from polltweet import PollTweet, Tweet
from pollparse import PollParse
import json
import logging

def main():

    with open('credentials.config') as file:
        credentials = json.load(file)
        twitter_credentials = credentials['twitter_credentials']

    polltweet = PollTweet(twitter_credentials['consumer_key'],
                          twitter_credentials['consumer_secret'],
                          twitter_credentials['access_token_key'],
                          twitter_credentials['access_token_secret'])
    
    poll_url = "http://elections.huffingtonpost.com/pollster/2016-general-election-trump-vs-clinton.csv"
    pollio = PollIO(poll_url, "./", "data.csv")
    
    new_polls = pollio.new_poll_data
    if new_polls is not None:
        tweet_list = []
        for row in new_polls.iterrows():
            row = row[1]
            tweet = Tweet(row['Pollster'], row['Start Date'], row['End Date'],
                          row['Clinton'], row['Trump'], row['Other'], row['Undecided'])
            tweet_list.append(tweet)

        #for tweet in tweet_list:
        #    polltweet.tweet_poll(tweet)

if __name__ == "__main__":
    main()

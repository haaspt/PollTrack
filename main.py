from __future__ import print_function
from pollio import PollIO
from polltweet import PollTweet
from pollparse import PollParse
import logging

def check_for_new_polls(url):

    latest_polls = pollio.get_latest_polls(url)
    old_polls = pollio.load_saved_polls()
    new_polls = pollio.new_polls(old_polls, latest_polls)
    if new_polls is None:
        return None
    else:
        pollio.save_poll_data(latest_polls)
        return new_polls

    
def main():

    poll_url = "http://elections.huffingtonpost.com/pollster/2016-general-election-trump-vs-clinton.csv"

    pollio = PollIO(poll_url, "./", "data.csv")

    new_polls = check_for_new_polls(poll_ulr)
    if new_polls is not None:
        tweet_new_polls()

if __name__ == "__main__":
    main()

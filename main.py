#!/usr/bin/env python
from __future__ import print_function

import json
import logging
import os.path
import os
import time
import schedule
from datetime import date

from pollio import PollIO
from pollparse import PollParse, FileLoadError
from polltweet import PollTweet, MediaTweet


class ConfigFileError(Exception):
    pass


def process_poll_list(poll_url_list, polltweet_instance):
    for state, poll_url in poll_url_list.items():
        get_and_tweet_new_polls(state, poll_url, polltweet_instance)


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
                    "{0}_data.csv".format(state).lower().replace(" ", "_")
                    )
    if pollio.latest_poll_data is not None:
        pollio.save_poll_data()
        
    if pollio.new_poll_data is not None:
        logger.debug("Attempting to tweet new polls")
        tweet_list = polltweet_instance.pandas_to_tweet(pollio.new_poll_data)
        polltweet_instance.tweet_polls(tweet_list)


def get_and_tweet_average_plot(state_name, polltweet_instance):
    """Calculates the 7 day rolling average of the national polls and creates a plot
    """

    data_file = "./data/" + state_name.lower().replace(" ", "_") + "_data.csv"
    if not os.isfile(data_file):
        logging.critical("Failed to load state data file, file does not exist: %s", data_file)
        raise FileLoadError
    
    logger.debug("Attempting to get data to average")
    try:
        list_of_dataframes = PollParse.load_dataframes(data_file)
    except FileLoadError as e:
        logging.critical('Error while loading file: %s', e)
        raise

    combined_dataframe = PollParse.combine_dataframes(list_of_dataframes)
    logger.debug("Parsing average poll data")
    polls = PollParse.parse_poll(combined_dataframe)
    avg = PollParse.rolling_average(polls)
    error = PollParse.rolling_error(polls)
    
    logger.debug("Plotting average poll data")
    plot = PollParse.plot_poll(polls, avg, error)
    plot_file = save_plot(plot)

    clinton_avg = round(avg['Clinton'].ix[avg.index.max()], 1)
    trump_avg = round(avg['Trump'].ix[avg.index.max()], 1)

    if state == "National":
        mediatweet = MediaTweet(clinton_avg, trump_avg, plot_file)
    else:
        mediatweet = MediaTweet(clinton_avg, trump_avg, plot_file, state=state_name)
        
    polltweet_instance.tweet_graph(mediatweet)


def save_plot(plot_object, filename=None):
    """Saves a pyplot figure to disk and returns the saved filename (+path)
    """
    
    if not os.path.exists('./figs/'):
        os.makedirs('./figs/')

    if filename is None:
        filename = './figs/avg_plot_' + str(date.today()) + '.png'

    plot_object.savefig(filename)
    return filename


def main():

    logger.info("PollTrack starting. Loading credentials")
    if not os.path.isfile('credentials.config'):
        logger.error("Credentials file not found")
        raise ConfigFileError("Credentials file not found, please see documentation for created a credential file")
    else:
        with open('./credentials.config') as infile:
            credentials = json.load(infile)
            twitter_credentials = credentials['twitter_credentials']
            infile.close()
            logger.debug("Credentials loaded")

    logger.info("Loading poll list")
    if not os.path.isfile('polls.json'):
        logger.error("Poll list file not found")
        raise ConfigFileError("Poll list file not found, please re-install or restore polls.json")
    else:
        with open('./polls.json') as infile:
            poll_file = json.load(infile)
            poll_url_list = poll_file['poll_list']
            infile.close()
            logger.debug("Poll list loaded")

    logger.info("Loading plot configuration")
    if not os.path.isfile('plots.config'):
        logger.error("Plot configuration file not found")
        raise ConfigFileError("Plot config file not found, please re-install or restore plots.config")
    else:
        with open('./plots.config') as infile:
            config_file = json.load(infile)
            plot_config = config_file['plot_config']
            infile.close()
            logger.debug("Plot config loaded")
            
    polltweet = PollTweet(twitter_credentials['consumer_key'],
                          twitter_credentials['consumer_secret'],
                          twitter_credentials['access_token_key'],
                          twitter_credentials['access_token_secret'])

    logger.info("Scheduling tasks")
    schedule.every(5).minutes.do(process_poll_list, poll_url_list, polltweet)
    for state, job_time in plot_config.iteritems():
        logger.info("Scheduling %s average plot", state)
        schedule.every().day.at(job_time).do(get_and_tweet_average_plot, [state, pollwteet])
    logger.info("Entering main loop")
    while True:
        schedule.run_pending()
        time.sleep(10)

        
if __name__ == "__main__":
    logging.basicConfig(filename='applog.log',
                        format='%(asctime)s-%(name)s :: %(levelname)s :: %(message)s',
                        level=logging.ERROR)
    logger = logging.getLogger(__name__)
    main()

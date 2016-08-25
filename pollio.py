from __future__ import print_function
import pandas as pd
import logging
import traceback


logger = logging.getLogger(__name__)

class PollIO(object):

    def __init__(self, poll_data_url, file_path, file_name):
        self.poll_data_url = poll_data_url
        self.file_path = file_path
        self.file_name = file_name

        self.latest_poll_data = self.get_latest_poll_data(self.poll_data_url)
        self.saved_poll_data = self.load_saved_poll_data()
        self.new_poll_data = self.new_polls(self.saved_poll_data, self.latest_poll_data)

    def get_latest_poll_data(self, csv_url):
        """Loads the latest polls from Huffington Post Pollster

        Parameters
        ----------
        csv_url: string
            The url to the longform csv to be loaded

        Returns
        -------
        pandas dataframe of the loaded data
        """
        try:
            logger.info('Downloading latest polls from web address')
            df = pd.read_csv(csv_url)
            logger.info('Downloaded data contains %d polls', len(df.index))
            return df
        except Exception as error:
            logger.error(traceback.format_exc())
            return None

    def save_poll_data(self, dataframe):
        """Saves a dataframe to the designated location

        Parameters
        ----------
        dataframe: pandas dataframe
            The dataframe to be saved

        Returns
        -------
        None
        """
        logger.info('Saving polls to disk')
        dataframe.to_csv(self.file_path + self.file_name, index=False)

    def load_saved_poll_data(self):
        """Loads a saved dataframe csv from disk

        Parameters
        ----------
        None

        Returns
        -------
        pandas dataframe of the loaded data
        """
        
        logging.info('Loading saved polls from disk')
        df = pd.read_csv(self.file_path + self.file_name)
        return df

    def new_polls(self, saved_poll_df, latest_poll_df):
        """Compares latest polls to those previously saved

        Parameters
        ----------
        saved_poll_df: pandas dataframe
            Old polls, previously scraped
        latest_poll_df: pandas dataframe
            Newest polls, which may or may not contain records not in the other

        Returns
        -------
        pandas dataframe containing the records only contained in the latest polls
        """
        #Applies a hash function to create a unqiue identifier for each poll/row in both dataframes
        latest_hash = latest_poll_df.apply(lambda x: hash(tuple(x)), axis=1)
        saved_hash = saved_poll_df.apply(lambda x: hash(tuple(x)), axis=1)

        #Returns rows from the latest poll dataframe whose hash value isn't in the last saved file
        new_polls_df = latest_poll_df[latest_hash.isin(saved_hash).apply(lambda x: not x)]
        logging.info('Latest poll data contained %d new polls.', len(new_polls_df.index))
        
        if len(new_polls_df.index) > 0:
            return new_polls_df
        else:
            return None


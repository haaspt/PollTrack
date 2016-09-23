import pandas as pd
import logging
import traceback
import os.path

from datetime import date, timedelta

pd.options.mode.chained_assignment = None  # Turns off Pandas copy warning

logger = logging.getLogger(__name__)


class PollIO(object):

    def __init__(self, state, poll_data_url, file_path, file_name):
        self.state = state
        self.poll_data_url = poll_data_url
        self.file_path = file_path
        self.file_name = file_name

        self.latest_poll_data = self.get_latest_poll_data()
        self.saved_poll_data = self.load_saved_poll_data()
        self.new_poll_data = self.return_new_polls(self.saved_poll_data, self.latest_poll_data)

    def get_latest_poll_data(self, csv_url=None):
        """Loads the latest polls from Huffington Post Pollster

        Parameters
        ----------
        csv_url: string, optional
            The url to the longform csv to be loaded
            Default: self.poll_data_url

        Returns
        -------
        pandas dataframe of the loaded data
        """
        try:
            logger.debug('Downloading latest %s polls from web address', self.state)
            if csv_url is None:
                csv_url = self.poll_data_url
            df = pd.read_csv(csv_url)
            # Extra formatting for state polls
            df['State'] = self.state
            if 'Other' not in df.columns:
                df['Other'] = 0.0
            if 'Johnson' in df.columns:
                df['Other'] = df['Johnson'] + df['Other']
            # End of extra formatting
            logger.debug('Downloaded data contains %d polls', len(df.index))
            self.latest_poll_data = df
            return self.latest_poll_data
        except Exception as error:
            logger.error(traceback.format_exc())
            return None

    def save_poll_data(self, dataframe=None, filename=None, filepath=None):
        """Saves a dataframe to the designated location

        Parameters
        ----------
        dataframe: pandas dataframe
            The dataframe to be saved
        filename: string, optional
            Name of the file stored to disk
            Default: self.file_name
        filepath: string, optional
            Path to folder to save data to
            Default: self.file_path
        """
        logger.debug('Saving polls to disk')
        if filename is None:
            filename = self.file_name
        if filepath is None:
            filepath = self.file_path
        if dataframe is None:
            dataframe = self.latest_poll_data
        dataframe.to_csv(filepath + filename, index=False)

    def load_saved_poll_data(self):
        """Loads a saved dataframe csv from disk

        Returns
        -------
        pandas dataframe of the loaded data
        """
        
        if os.path.isfile(self.file_path + self.file_name):
            logging.debug('Loading saved polls from disk')
            df = pd.read_csv(self.file_path + self.file_name)
            self.saved_poll_data = df
            return self.saved_poll_data
        else:
            logging.error('No saved datafile found, downloading latest data')
            df = self.get_latest_poll_data()
            self.save_poll_data(df)
            self.saved_poll_data = df
            return self.saved_poll_data

    def return_new_polls(self, saved_poll_df, latest_poll_df):
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
        # Applies a hash function to create a unqiue identifier for each poll/row in both dataframes
        latest_hash = latest_poll_df.apply(lambda x: hash(tuple(x)), axis=1)
        saved_hash = saved_poll_df.apply(lambda x: hash(tuple(x)), axis=1)

        # Returns rows from the latest poll dataframe whose hash value isn't in the last saved file
        new_polls_df = latest_poll_df[latest_hash.isin(saved_hash).apply(lambda x: not x)]
        
        if len(new_polls_df.index) > 0:
            logging.info('Possible new polls found for %s', self.state)
            logging.info('Hash comparison indicates %d new polls.', len(new_polls_df.index))
            new_polls_df['Start Date'] = pd.to_datetime(new_polls_df['Start Date'])
            new_polls_df['End Date'] = pd.to_datetime(new_polls_df['End Date'])
            new_polls_df = new_polls_df.fillna(0)
            # This prevents the posting of any poll with an end date older than a week ago
            lastweek = date.today() - timedelta(7)
            new_polls_df = new_polls_df[new_polls_df['End Date'] >= lastweek]
            logging.info('%d polls found within the last 7 days', len(new_polls_df.index))
            
            if len(new_polls_df.index) == 0:
                self.new_poll_data = None
                return None
            
            self.new_poll_data = new_polls_df
            return self.new_poll_data
        else:
            self.new_poll_data = None
            return None

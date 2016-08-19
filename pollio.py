from __future__ import print_function
import pandas as pd

class PollIO(object):

    def __init__(self, poll_data_url, file_path, file_name):
        self.poll_data_url = poll_data_url
        self.file_path = file_path
        self.file_name = file_name

        self.latest_poll_data = self.latest_poll_data(self.poll_data_url)
        self.saved_poll_data = self.load_saved_poll_data(self.file_path, self.file_name)
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
        df = pd.read_csv(csv_url)
        return df

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
        # Compare the two frames and only return those added since last save
        return new_polls_df

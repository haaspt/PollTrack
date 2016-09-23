from __future__ import division
import pandas as pd
import logging
import os.path

pd.options.mode.chained_assignment = None  # Turns off Pandas copy warning

logger = logging.getLogger(__name__)


class FileLoadError(Exception):
    pass


class PollParse(object):

    @staticmethod
    def load_dataframe(*filepaths):
        """Loads a series of saved CSV files from disk and returns them as a list of pandas dataframes

        Parameters
        ----------
        *filepaths: string
            An arbitrary number of filepaths to the dataframes to be loaded

        Returns
        -------
        list of pandas dataframes
        """

        for filepath in filepaths:
            if not os.path.isfile(filepath):
                raise FileLoadError('Specified file does not exist: %s', filepath)

        list_of_dataframes = map(lambda x: pd.read_csv(x), [filename for filename in filepaths])
        return list_of_dataframes

    @staticmethod
    def combine_polls(list_of_dataframes):
        """Combines multiple dataframes into one

        Parameters
        ----------
        list_of_dataframes: list of pandas dataframes
            
        Returns
        -------
        pandas dataframe of the combined data
        """

        frames = list_of_dataframes
        combined_df = pd.concat(frames)
        return combined_df

    @staticmethod
    def rolling_average(dataframe):

        dataframe.resample('1d').median().rolling(window=7, min_periods=1).mean().fillna(method='ffill')
        return dataframe

    @staticmethod
    def parse_poll(dataframe):
        """Performs a series of transformations and filters on the poll dataframe to prepare it for a rolling average.
        The following steps are take:
        1. Polls that target specific voter groups (Republican, Democrat, Independent) are filtered out
        2. The Start and End Date columns are transformed to datetime format
        3. The index is set to be the average time between the poll's start and end dates
        4. Unnecessary columns are discarded
        5. NAN values are replaced with 0.0

        Parameters
        ----------
        dataframe: pandas dataframe

        Returns
        -------
        pandas dataframe ready for rolling average
        """

        df = dataframe[~dataframe['Population'].str.contains('Republican') &
                       ~dataframe['Population'].str.contains('Democrat') &
                       ~dataframe['Population'].str.contains('independent')]  # I know that's not capitalized

        df[['Start Date', 'End Date']] = df[['Start Date', 'End Date']].apply(lambda x: pd.to_datetime(x))

        df.index = df['End Date'] - ((df['End Date'] - df['Start Date']) / 2)

        valid_column_labels = ['Clinton', 'Trump', 'Johnson', 'Stein', 'Undecided', 'Other']
        available_column_labels = df.columns
        present_column_labels = [label for label in available_column_labels if label in valid_column_labels]

        df = df[present_column_labels]

        df = df.fillna(0)

        return df

from __future__ import print_function
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class PollParse(object):

    def combine_polls(self, dataframe1, dataframe2):
        """Combines two dataframes of polling data

        Parameters
        ----------
        dataframe1, dataframe2: pandas dataframes
            
        Returns
        -------
        pandas dataframe of the combined data
        """

        #Actual code should go here
        return combined_df

    def rolling_average(self, dataframe):

        #This code doesn't work yet
        dataframe.resample('1d').median().rolling(window=14, min_period=1).mean().fillna(method='ffill')
        return dataframe

#

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class Mondriaan(object):

    def __init__(self):

        self.history = None

    def setup_df(self, df, freq='D'):
        """setup dataframe for prediction.

        Parameters
        ----------
        df: pd.DataFrame with columns t, y

        Returns
        -------
        pd.DataFrame prepared for prediction.
        """
        if ('t' not in df) or ('y' not in df):
            raise ValueError(
                '* Dataframe must have columns "t" and "y" with the dates and '
                'values respectively.'
            )
        df = df[df['y'].notnull()][['t', 'y']]

        if len(df) < 4:
            raise ValueError(
                '* The dataframe must have a minimum of 4 non-NaN rows.')

        df['y'] = pd.to_numeric(df['y'])

        if np.isinf(df['y'].values).any():
            raise ValueError('* Found infinities in column y.')

        if df['t'].dtype == np.int64:
            df['t'] = df['t'].astype(str)

        df['t'] = pd.to_datetime(df['t'])
        if df['t'].isnull().any():
            raise ValueError('* Found NaNs in column t.')

        if df.index.name == 't':
            df.index.name = None
        df = df.sort_values('t')
        df = df.reset_index(drop=True)  # .set_index('t')

        return df

    def fit(self, df, freq=None, method=None):
        """Fit the Nostradamus model.

        """

        if self.history is not None:
            raise Exception('* Nostradamus object can only be fit once. '
                            'Consider instantiating a new object.')

        history = df.copy()
        self.history = self.setup_df(history)

        if freq is not None:
            self.history = self.history.set_index(
                't').groupby(pd.Grouper(freq=freq)).mean()
            if len(self.history) > len(history):
                print('* Warning: freq is larger than the original dataframe freq.')
            elif len(self.history) < len(history):
                print('* Warning: freq is shorter than the original dataframe freq.')
            else:
                print(
                    '* The parameter \'freq\' has the same value as in the original dataframe freq.')

        if method is not None:
            print(
                '* You chose to fill the missing values in the dataframe with \'{}\'.'.format(method))
            self.history = self.history.fillna(method=method)

        self.history_dates = history.t
        self.history_values = history.y

        print(self.history.tail(4))

    def predict(self, periods=None, freq=None, method=None):
        if periods is not None and freq is not None:
            print('* The parameter \'freq\' must be the same as in the fitted dataframe.')
            future = self.history
            self.future = pd.DataFrame(pd.date_range(
                start=future.index[-1], periods=periods + 1, freq=freq)[1:], columns=['f'])

        # print(self.future)

        if method is not None:
            if method == 'last value':
                print(
                    '* Forecasting future values using the \'{}\' method over {} periods with frequency \'{}\'.'.format(method, periods, freq))
                self.future['y'] = self.history['y'].iloc[-1]

            if method == 'last freq':
                if freq == 'Q':
                    self.future['y'] = self.history.resample(
                        'Q').asfreq()[-4:].values

        else:
            print('Applying magic sauce...')

        print(self.future)

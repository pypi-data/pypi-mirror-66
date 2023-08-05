#

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.path.append('/Users/naftali/nostradamus')  # path to nostradamus library
from nostradamus.forecaster import Nostradamus


directory = '/Users/naftali/nostradamus/datasets/'
filename = 'AusBeer.csv'
df = pd.read_csv(directory + filename)

n = Nostradamus()
#############
freq = 'Q'  # e.g. None, 'A', 'Q', '3M', 'M', 'D','B'
fillnan_method = 'ffill'  # e.g. None, 'ffill'
n.fit(df, freq, fillnan_method)
#############

future_periods = 4
future_freq = 'Q'
forecasting_method = 'last freq'  # e.g. 'last value','last freq'
n.predict(future_periods, future_freq, forecasting_method)
#################
# n.plot()

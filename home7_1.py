
# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkstudy.EventProfiler as ep

# Third Party Imports
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import copy
import math
import csv

def bollinger():
    '''Main Function'''
    # List of symbols
    ls_symbols =dataobj.get_symbols_from_list('sp5002012')
    ls_symbols.append('SPY')

    # Start and End date of the charts
    dt_start = dt.datetime(2008, 1, 1)
    dt_end = dt.datetime(2009, 12, 31)

    # We need closing prices so the timestamp should be hours=16.
    dt_timeofday = dt.timedelta(hours=16)

    # Get a list of trading days between the start and the end.
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)

    # Creating an object of the dataaccess class with Yahoo as the source.
    c_dataobj = da.DataAccess('Yahoo')

    # Keys to be read from the data, it is good to read everything in one go.
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

    # Reading the data, now d_data is a dictionary with the keys above.
    # Timestamps and symbols are the ones that were specified before.
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    # Copying close price into separate dataframe to find rets
    df_close = d_data['close']
    df_mean = pd.rolling_mean(d_data['close'], 20)
    df_std = pd.rolling_std(d_data['close'], 20)
    df_bollinger = (df_close - df_mean) / (df_std)
    
    return df_bollinger   

def find_events(ls_symbols, d_data, df_bollinger):
     ''' Finding the event dataframe '''
     df_close = d_data['close']
     ts_market = df_bollinger['SPY']
     print "Finding Events"

     # Creating an empty dataframe
     df_events = copy.deepcopy(df_close)
     df_events = df_events * np.NAN

     # Time stamps for the event range
     ldt_timestamps = df_close.index

     for s_sym in ls_symbols:
        for i in range(1, len(ldt_timestamps)):
            # Calculating the returns for this timestamp
            f_bollinger_today = df_bollinger[s_sym].ix[ldt_timestamps[i]]
            f_bollinger_yest = df_bollinger[s_sym].ix[ldt_timestamps[i - 1]]
            f_bollinger_market_today = ts_market.ix[ldt_timestamps[i]]
            
            f_cutoff = -2.0
            if f_bollinger_today <= f_cutoff and f_bollinger_yest >= f_cutoff and f_bollinger_market_today >= 1.0:
                 with open('orders3.csv', 'a') as fp:
		    a1 = csv.writer(fp, delimiter=',')
  		    row = [[ldt_timestamps[i] ,s_sym,'Buy',100], ['2009-12-31','16:00:00',s_sym,'Sell',100]]
 	     	    a1.writerows(row)
     return df_events


if __name__ == '__main__':
    dt_start = dt.datetime(2009, 12, 24)
    dt_end = dt.datetime(2009, 12, 31)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

    dataobj = da.DataAccess('Yahoo')
    ls_symbols = dataobj.get_symbols_from_list('sp5002012')
    ls_symbols.append('SPY')
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method = 'ffill')
        d_data[s_key] = d_data[s_key].fillna(method = 'bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    df_events = find_events(ls_symbols, d_data, df_bollinger = bollinger())
    print "Creating Study"

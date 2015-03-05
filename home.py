import pandas as pd
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
from pylab import *
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import csv
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def _csv_read_goog_adjusted_close_dates(filename):
    reader = csv.reader(open(filename, 'rU'), delimiter=',')
    goog_close = []
    dates = []
    rolling_mean = [] 
    std = []
    upper = []
    lower = []
    indicator_value = []
    for row in reader:
        if not(row[8] in goog_close):
            goog_close.append(row[8])
        date = dt.datetime(int(row[0]), int(row[1]), int(row[2]))
        if not(date in dates):
            dates.append(date)
	if not(row[9] in rolling_mean):
	    rolling_mean.append(row[9])
	if not(row[10] in std):
	    std.append(row[10])
	if not(row[11] in upper):
	    upper.append(row[11])
	if not(row[12] in lower):
	    lower.append(row[12])
	if not(row[13] in indicator_value):
	    indicator_value.append(row[13])
    dates = sorted(dates)
    return goog_close, dates, rolling_mean, std, upper, lower, indicator_value

goog_close, dates, rolling_mean, std, upper, lower, indicator_value = _csv_read_goog_adjusted_close_dates(sys.argv[1])


testFigure = plt.figure(1)
plt.subplot(211)
plt.plot(dates,goog_close)
plt.plot(dates,upper)
plt.plot(dates,lower)

plt.subplot(212)
plt.plot(dates, indicator_value)
pp = PdfPages('home.pdf')
testFigure.savefig(pp, format='pdf')
pp.close()

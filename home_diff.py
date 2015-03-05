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
        for row in reader:
        if not(row[8] in goog_close):
            goog_close.append(row[8])
        date = dt.datetime(int(row[0]), int(row[1]), int(row[2]))
        if not(date in dates):
            dates.append(date)
    dates = sorted(dates)
    return goog_close, dates

goog_close, dates = _csv_read_goog_adjusted_close_dates(sys.argv[1])

rolling_mean = []

for i in len(goog_close):
    rolling_mean[i] = (goog_close[i-20]+goog_close[i-19]+goog_close[i-18]+goog_close[i-17]+goog_close[i-16]+goog_close[i-15]+goog_close[i-14]+goog_close[i-13]+goog_close[i-12]+goog_close[i-11]+goog_close[i-10]+goog_close[i-9]+goog_close[i-8]+goog_close[i-7]+goog_close[i-6]+goog_close[i-5]+goog_close[i-4]+goog_close[i-3]+goog_close[i-2]+goog_close[i-1])/20.0
    std[i] = numpy.std(a,)
upper = []
lower = []
indicator_value = []

	

testFigure = plt.figure(1)
plt.subplot(211)
plt.plot(dates,goog_close)
plt.plot(dates,upper)
plt.plot(dates,lower)

plt.subplot(212)
plt.plot(dates, indicator_value)
pp = PdfPages('home1.pdf')
testFigure.savefig(pp, format='pdf')
pp.close()

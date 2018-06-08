from Stock_extract import extraction
import matplotlib.pyplot as plt
import seaborn; seaborn.set()
from pandas.plotting import autocorrelation_plot
from statsmodels.tsa.arima_model import ARIMA
import pandas as pd

df=extraction()
print('There are 7 stockes plot you could select: ')
print(df.columns)


def global_plot(stock):
    if stock is 'all':
        plt.plot(df).area()
        plt.xlabel('time')
        plt.legend(df.columns)
        plt.show()

    else:
        plt.plot(df[stock],label=stock)
        plt.xlabel('time')
        plt.legend()
        plt.show()


def trend(stock):
    #Remove the seasonal pattern only left trend
    plt.plot(df[stock].rolling(24).mean(),label='%s Trend' %stock)
    plt.xlabel('time')
    plt.legend()
    plt.show()

def season(stock):
    plt.plot(df[stock].diff(),label='%s Seasonal Pattern' %stock)
    plt.xlabel('time')
    plt.legend()
    plt.show()


df.plot.area()
plt.show()
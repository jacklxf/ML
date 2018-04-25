import quandl
import datetime
import numpy as np
import pandas as pd

names_list=pd.read_csv('/home/lxf/Documents/Data/companylist.csv')
Symbol_list=names_list['Symbol']

quandl.ApiConfig.api_key = '2YacMQGW7xL6qTi_bVss'
def quandl_stocks(symbol, start_date=(2015, 1, 1), end_date=None):
    """
    symbol is a string representing a stock symbol, e.g. 'AAPL'

    start_date and end_date are tuples of integers representing the year, month,
    and day

    end_date defaults to the current date when None
    """

    query_list = ['WIKI' + '/' + symbol + '.' + str(k) for k in range(1, 13)]

    start_date = datetime.date(*start_date)

    if end_date:
        end_date = datetime.date(*end_date)
    else:
        end_date = datetime.date.today()

    return quandl.get(query_list,returns='pandas',start_date=start_date,end_date=end_date,collapse='daily',order='asc')

def load_data(data):
    data.to_csv("/home/lxf/Documents/Data/stocks")

if __name__ == '__main__':
    #print(quandl_stocks('AAPL'))
    for i in Symbol_list:
        df=pd.DataFrame(quandl_stocks(i))
        print(df.head())
        df=quandl_stocks(i)
        load_data(data=df)
        print(i+' has been downloaded and saved.')
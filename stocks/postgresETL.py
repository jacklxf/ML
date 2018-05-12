<<<<<<< HEAD
import numpy as npimport pandas as pdimport quandlimport datetimefrom sqlalchemy import create_enginehost='localhost'dbname='postgres'user='postgres'password='wenqian628'engine = create_engine('postgresql://postgres:wenqian628@localhost:5432/postgres')quandl.ApiConfig.api_key = '2YacMQGW7xL6qTi_bVss'def quandl_stocks(symbol, start_date=(2018, 1, 1), end_date=None):        #symbol is a string representing a stock symbol, e.g. 'AAPL'    #start_date and end_date are tuples of integers representing the year, month,    #and day    #end_date defaults to the current date when None        query_list = ['WIKI' + '/' + symbol + '.' + str(k) for k in range(1, 13)]    start_date = datetime.date(*start_date)    if end_date:        end_date = datetime.date(*end_date)    else:        end_date = datetime.date.today()    return quandl.get(query_list,                      returns='pandas',                      start_date=start_date,                      end_date=end_date,                      collapse='daily',                      order='asc'                      )Symbol_name=pd.read_csv('/home/xf/Documents/ML/stocks/companylist.csv')n=Symbol_name['Symbol']for i in n.values:    try:        df = quandl_stocks(str(i))        df.columns = [c.lower() for c in df.columns]        df.to_sql(i, engine)        print(i + ' has done!')    except ValueError:        print(i+' is failed')        pass
=======
import numpy as np
import pandas as pd
import quandl
import datetime
from sqlalchemy import create_engine

host='localhost'
dbname='postgres'
user='postgres'
password='wenqian628'
engine = create_engine('postgresql://postgres:wenqian628@localhost:5432/postgres')

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

    return quandl.get(query_list,
                      returns='pandas',
                      start_date=start_date,
                      end_date=end_date,
                      collapse='daily',
                      order='asc'
                      )


Symbol_name=pd.read_csv('/home/xf/Documents/ML/stocks/companylist.csv')
n=Symbol_name['Symbol']
for i in n.values:
    try:
        df = quandl_stocks(str(i))
        df.columns = [c.lower() for c in df.columns]
        df.to_sql(i, engine)
        print(i + ' has done!')
    except ValueError:
        print(i+' is failed')
        pass






>>>>>>> 880eb8407d5c21bbcbd8795ab720a1485b763a24

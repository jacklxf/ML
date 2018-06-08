import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import quandl
from sqlalchemy import create_engine
import datetime


host='localhost'
dbname='postgres'
user='postgres'
password='wenqian628'
engine = create_engine('postgresql://postgres:wenqian628@localhost:5432/postgres')
quandl.ApiConfig.api_key = '2YacMQGW7xL6qTi_bVss'

Symbol_name=pd.read_csv('companylist.csv')
tickers=Symbol_name['Symbol']
tickers=['FDX','TMUS','MSFT','AAPL','GOOGL','FB','TWTR']
start_date='2010-1-1'
for i in tickers:
    try:
        df=quandl.get("WIKI/"+str(i),returns='pandas',collapse='daily',start_date=start_date,end_date = datetime.date.today()).reset_index()
        df.columns=[c.lower() for c in df.columns]
        df.to_sql(i.lower(), engine,if_exists='replace')
        print(i+" has done!")
    except ValueError:
        print(i + ' is failed')
        pass


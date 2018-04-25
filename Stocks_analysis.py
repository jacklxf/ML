import quandl
import datetime
import psycopg2
import sys

postgres_insert=("""
    INSERT INTO AAPL ('WIKI/AAPL - Open', 'WIKI/AAPL - High', 'WIKI/AAPL - Low',
       'WIKI/AAPL - Close', 'WIKI/AAPL - Volume', 'WIKI/AAPL - Ex-Dividend',
       'WIKI/AAPL - Split Ratio', 'WIKI/AAPL - Adj. Open',
       'WIKI/AAPL - Adj. High', 'WIKI/AAPL - Adj. Low',
       'WIKI/AAPL - Adj. Close', 'WIKI/AAPL - Adj. Volume')
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
)

conn_string = {'host': 'localhost',
               'dbname': 'postgres',
               'user': 'postgres',
               'password': 'wenqian628'}

quandl.ApiConfig.api_key = '2YacMQGW7xL6qTi_bVss'

def quandl_stocks(symbol, start_date=(2018, 1, 1), end_date=None):
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


def load_data(data):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cursor.executemany(postgres_insert, data.valules.tolist())
    cursor.close()
    conn.close()

if __name__ == '__main__':
    df = quandl_stocks('AAPL')
    print('Extraction done.')
    load_data(data=df)
    print('Load done.')
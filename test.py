
import quandl
import datetime
import psycopg2
import sys

conn_string = {'host': 'localhost',
               'dbname': 'stocks',
               'user': 'postgres',
               'password': 'wenqian628',}

conn = psycopg2.connect(conn_string)
cursor = conn.cursor()
#cursor.executemany(postgres_insert, data.valules.tolist())
cursor.close()
conn.close()
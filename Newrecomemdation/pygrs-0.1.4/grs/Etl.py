import pymssql
import cx_Oracle
from pyspark.sql.session import SparkSession
from pandas import HDFStore

class etl():
    def __init__(self):
        self.spark = SparkSession.builder.getOrCreate()

    def read_sql_data(self, args, sql_query, schema):
        conn = pymssql.connect(args.server, args.loginName, args.password, schema)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        return cursor.fetchall()

    def read_oracle_data(self, args, sql_query):
        dsn_tns = cx_Oracle.makedsn(args.ip, args.port, args.sid)
        conn = cx_Oracle.connect(args.userName, args.password, dsn_tns)
        cursor = conn.cursor()
        return cursor.fetchall()

    def write_hdfs(self, data_dict, path):
        store = HDFStore(path)
        for key, value in data_dict.items():
            store.put(key, value)
        store.close()

    def append_hdfs(self, df, path, key):
        try:
            store = HDFStore(path)
            store.append(key, df)
        except:
            print("Error for appending data to {0} in {1}".format(key, path))


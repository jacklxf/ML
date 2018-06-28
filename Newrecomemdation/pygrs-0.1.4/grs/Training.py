import pickle
import pandas as pd
from pyspark.sql.session import SparkSession
from pyspark import SparkContext
from pyspark.sql.functions import *

class data_source():
    def read_data(self, path, key):
        try:
            return pd.read_hdf(path, key)
        except Exception as e:
            print("Error reading data from {0} in {1}".format(key, path))
            print(e)

    # for generating dictionary when int id is needed
    def bimap(self, list):
        return dict([(y, x + 1) for x, y in enumerate(list)])

    def reverse(self, dict):
        return {i[1]: i[0] for i in dict.items()}

class model_store():
    def __init__(self):
        self.sc = SparkContext().getOrCreate()
        self.spark = SparkSession.builder.getOrCreate()

    def store_models_local(self, path, model):
        try:
            with open(path, 'wb') as handle:
                pickle.dump(model, handle, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            print("Error: {0}".format(e))

    def read_models_local(self, path):
        try:
            with open(path, 'rb') as handle:
                return pickle.load(handle)
        except Exception as e:
            print("Error: {0}".format(e))

    def store_models_hdfs(self, path, model):
        self.sc.parallelize([model]).saveAsTextFile(path)

    def read_models_hdfs(self, path):
        for i in range(1, 5):
            while True:
                try:
                    return eval(self.sc.textFile(path).collect()[0])
                except Exception as e:
                    print("Error: {0}".format(e))
                    print("retry: {0}".format(i))
                    continue

from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql.types import StringType
from pyspark import SQLContext
import numpy as np
import pandas as pd
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.linalg.distributed import RowMatrix
from pyspark.sql import SQLContext


conf=SparkConf('local')
sc=SparkContext(conf=conf)
sql_sc=SQLContext(sc)
df=pd.read_csv('C:/Google Drive/Work Scrip Code/Data/ratings_xf.csv')
df=sql_sc.createDataFrame(df)
print(df.show())

R_df=df.groupBy('userID').pivot('subgameID').agg('rating')
mat=RowMatrix(R_df)
svd=mat.computeSVD(5,computeU=True)
U=svd.U
S=svd.S
V=svd.V

print(U,S,V)

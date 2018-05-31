# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import findspark
findspark.init()
import pyspark
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
spark=SparkSession.builder.getOrCreate()
sc=spark.sparkContext

df=pd.read_csv('C:/Users/xiaofeng.li/Google Drive/Data/AI-Data.csv')
df=df[['PlayerID','GameID','BetAmount']]
df_spark=spark.createDataFrame(df)
#df_spark.show(20)

user_sum=df_spark.groupby('PlayerID').sum('BetAmount')
user_sum=user_sum.select(F.col('PlayerID').alias("PlayerID"),F.col('sum(BetAmount)').alias("totalAmt"))

df_group=df_spark.groupby('PlayerID','GameID').sum('BetAmount')
df_group=df_group.select(F.col('PlayerID').alias('PlayerID'),F.col('GameID').alias('GameID'),F.col('sum(BetAmount)').alias('amt'))

data=df_group.join(user_sum,on=['PlayerID'],how='left_outer')
#data.show(20)

data=data.withColumn('rate',(F.col("amt"))/(F.col("totalAmt"))*10).drop("amt","totalAmt")
#data.show(20)

rating=data.toPandas()

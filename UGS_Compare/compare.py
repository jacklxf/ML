import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse



ourea=pd.read_csv('C://Users//xiaofeng.li.AFTG//Documents//ML//UGS_Compare//ourea.csv')
ugs=pd.read_csv('C://Users//xiaofeng.li.AFTG//Documents//ML//UGS_Compare//ugs.csv')
print(ourea.head())
print(ugs.head())


"""
amtlog=amtlog[['FTRANSID','username','game_name','FAMOUNT']]
amtlog_user=amtlog[amtlog['game_name']==games][['username','FAMOUNT']].groupby('username').sum().reset_index()
amtlog_user['FAMOUNT']=round(amtlog_user['FAMOUNT'],2)

eb1=eb1[['Login Name',wallet]]
eb1_group=eb1.groupby('Login Name').sum().reset_index()
eb1_group.columns=["user1","main1"]
eb2=eb2[['Login Name',wallet]]
eb2_group=eb2.groupby('Login Name').sum().reset_index()
eb2_group.columns=['user2','main2']
eb=pd.merge(eb1_group,eb2_group,left_on='user1',right_on='user2',how='outer').fillna(0)
eb['main']=round(eb['main2']-eb['main1'],2)


df=pd.merge(amtlog_user,eb,left_on='username',right_on='user2',how='outer')
df=df.fillna(0)
print(df.isnull().any())
df.to_csv('C:/Users/xiaofeng.li/Documents/ML/amtlog_endbalance/result.csv')
"""


import numpy as np
import pandas as pd

#create amtlog table
amtlog=pd.read_csv('C:/Users/xiaofeng.li/Downloads/amtlog/amtlog19.csv')
amtlog=amtlog[(amtlog.game_name=='OneLab Sportbook') & (amtlog.FCURRENCY=='VND')]
amtlog=amtlog.drop(['game_name','FCURRENCY'],1)
amtlog_group=amtlog.groupby('username').sum()
amtlog=amtlog_group.reset_index()
amtlog.to_csv('amtlog.csv')

#create endbalance table
endbalance18=pd.read_csv('C:/Users/xiaofeng.li/Downloads/endbalance/endbalance18.csv')
endbalance19=pd.read_csv('C:/Users/xiaofeng.li/Downloads/endbalance/endbalance19.csv')

endbalance=endbalance18.merge(endbalance19,left_on='Login Name',right_on='Login Name',how='outer').fillna(0)
endbalance.columns=['username','balance18','balance19']
endbalance['FAMOUNT']=endbalance['balance19']-endbalance['balance18']
endbalance=endbalance.drop(['balance18','balance19'],1)
endbalance.to_csv('C:/Users/xiaofeng.li/Downloads/endbalance.csv')


for m in range(0,len(endbalance)):
    if endbalance.values[m] not in amtlog.values:
        print(endbalance.values[m])
print('it is in endbalance not in amtlog')

for m in range(0,len(amtlog)):
    if amtlog.values[m] not in endbalance.values:
        print(amtlog.values[m])
print('it is in amtlog not in endbalance')
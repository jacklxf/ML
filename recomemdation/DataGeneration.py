import numpy as np
import pandas as pd

data=pd.read_csv('C:/Users/xiaofeng.li.AFTG/Downloads/AI-Data.csv')
print(data.head())

def DataRatingGene(rawdata=data):
    data=rawdata[['GameID','PlayerID','BetAmount']]
    user_sum=data.groupby(['PlayerID'])['BetAmount'].sum()
    data_group=data.groupby(['PlayerID','GameID'])['BetAmount'].sum()
    rating=pd.DataFrame(index=range(0,data_group.size),columns=['userID','subgameID','rating'])

    for i in range(0,len(rating.index)):
        rating.iloc[i,0]=data_group.index[i][0]
        rating.iloc[i,1]=data_group.index[i][1]
        rating.iloc[i,2]=(data_group.iloc[i]/user_sum.get(data_group.index[i][0]))*10
    print(rating.head())

    return rating

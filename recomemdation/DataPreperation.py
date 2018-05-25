#from DataGeneration import *
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

rating=pd.read_csv('C:/Users/xiaofeng.li.AFTG/Google Drive/Data/rating.csv')
rating=rating[['PlayerID','GameID','rate']]
print('rating.csv reading done.')
print(rating.columns)
MNS=MinMaxScaler()
rating_scaler=MNS.fit_transform(rating['rate'].values.reshape(-1,1))
rating_scaler=pd.DataFrame(rating_scaler)
rating['rate']=rating_scaler
print(rating.head())
rating_matrix=rating.pivot(index='PlayerID',columns='GameID',values='rate').fillna(0)
print('This is rating_matrix done.')

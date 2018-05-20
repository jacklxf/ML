from DataGeneration import *
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

rating=DataRatingGene()

def scaler():
    MNS=MinMaxScaler()
    rating_scaler=MNS.fit_transform(rating['rating'].values.reshape(-1,1))
    rating_scaler=pd.DataFrame(rating_scaler)
    rating['rating']=rating_scaler
    rating_matrix=rating.pivot(index='userID',columns='subgameID',values='rating').fillna(0)
    print('This is rating_matrix data:')
    print(rating_matrix.head())
    return rating_matrix

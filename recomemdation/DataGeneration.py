import numpy as np
import pandas as pd

games=pd.read_csv('C://Users//xiaofeng.li//Google Drive//Work Scrip Code//Recommendation//cl_game_id_name_sss_201710.csv')
events=pd.read_csv('C://Users//xiaofeng.li//Google Drive//Work Scrip Code//Recommendation//cl_bethist_sss_201710_aa.csv')
data=pd.merge(events,games,how="left",left_on=['FSUBGAMEID'],right_on=['FID'])

def DataRatingGene(rawdata=data):
    data=rawdata[['FSUBGAMEID_x','FUSERID','FBETAMT']]
    user_sum=data.groupby(['FUSERID'])['FBETAMT'].sum()
    data_group=data.groupby(['FUSERID','FSUBGAMEID_x'])['FBETAMT'].sum()
    rating=pd.DataFrame(index=range(0,data_group.size),columns=['userID','subgameID','rating'])

    for i in range(0,len(rating.index)):
        rating.iloc[i,0]=data_group.index[i][0]
        rating.iloc[i,1]=data_group.index[i][1]
        rating.iloc[i,2]=(data_group.iloc[i]/user_sum.get(data_group.index[i][0]))*10
    print(rating.head())

    return rating

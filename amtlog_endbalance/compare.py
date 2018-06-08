import pandas as pd
import argparse


print('Example:')
print("amtlog_name='SSS988_20180602.csv'")
print("eb1_name='SSS988_EndBalanceDetail_RMB_20180601.csv'")
print("eb2_name='SSS988_EndBalanceDetail_RMB_20180602.csv'")
print("games='Sport Book'")
print("wallet='SPORTBOOK BALANCE'")

parser = argparse.ArgumentParser()
amtlog_name=parser.add_argument('--amtlog_name',required=True)
eb1_name=parser.add_argument('--eb1_name',required=True)
eb2_name=parser.add_argument('--eb2_name',required=True)
games=parser.add_argument('--games',required=True)
wallet=parser.add_argument('--wallet',required=True)

def main():

    amtlog=pd.read_csv("C:/Users/xiaofeng.li/Documents/ML/amtlog_endbalance/%s" %amtlog_name,encoding='ISO-8859-1')
    eb1=pd.read_csv("C:/Users/xiaofeng.li/Documents/ML/amtlog_endbalance/%s" %eb1_name)
    eb2=pd.read_csv("C:/Users/xiaofeng.li/Documents/ML/amtlog_endbalance/%s" %eb2_name)


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

if __name__ == '__main__':
    main()


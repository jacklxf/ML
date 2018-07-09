import pandas as pd
import argparse


'''
example:

python amtlog_endbalance_compare.py "SSS988_20180702.csv" "SSS988_EndBalanceDetail_RMB_20180701.csv" "SSS988_EndBalanceDetail_RMB_20180702.csv" "UGS" "UGS
 BALANCE"
'''

parser=argparse.ArgumentParser()
parser.add_argument('amtlog_name',help='the amtlog csv file name',type=str)
parser.add_argument('eb1_name',help='the previous endbalance file name',type=str)
parser.add_argument('eb2_name',help='the current endbalance file name',type=str)
parser.add_argument('games',help='games name in amtlog file',type=str)
parser.add_argument('wallet',help='the game wallet name in endbalance',type=str)

args=parser.parse_args()

amtlog_name=str(args.amtlog_name)
eb1_name=str(args.eb1_name)
eb2_name=str(args.eb2_name)
games=str(args.games)
wallet=str(args.wallet)

def main():

    amtlog=pd.read_csv(amtlog_name,encoding='ISO-8859-1')
    eb1=pd.read_csv(eb1_name)
    eb2=pd.read_csv(eb2_name)


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
    #print(df.head())
    df['diff']=df['FAMOUNT']-df['main']
    print(df.isnull().any())
    df=df[df['diff']!=0]
    print(df)
    df.to_csv('C:/Users/xiaofeng.li/Documents/ML/amtlog_endbalance/result.csv')

if __name__ == '__main__':
    main()


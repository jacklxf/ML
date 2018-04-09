import numpy as np
import pandas as pd

def adjustDate():
    df = pd.read_excel('C:/Users/xiaofeng.li/Downloads/Jan2018.xlsx', header=0)
    df.Date = pd.DatetimeIndex(df.Date).normalize()
    P_adjust=[]
    for num in range(1, 32):
        amt = round(sum(df['Amount'][(df.Tag == 'Bonus Adjustment') & (df.Date == '2018-01-%s' % num)]) + sum(
            df['Amount'][(df.Tag == 'Cut Bonus Adjustment') & (df.Date == '2018-01-%s' % num)]))
        P_adjust.append(amt)
    
    df_adjust = pd.read_csv('C:/Users/xiaofeng.li/Downloads/JAN2018_S_ADJUST.csv')
    df_adjust['DT'] = pd.to_datetime(df_adjust.DT)
    S_adjust = []
    for num in range(1, 32):
        amt =round(sum(df_adjust['BONUS'][df_adjust.DT == '%s-JAN-18' % num]))
        S_adjust.append(amt)
    
    compare=pd.DataFrame(columns=['date','P_adjust','S_adjust'])
    date=pd.date_range('2018-1-1','2018-1-31')
    compare['date']=date
    compare['P_adjust']=P_adjust
    compare['S_adjust']=S_adjust
    
    dt=[]
    for n in range(0,len(compare)):
        if compare.iloc[n,1] != compare.iloc[n,2]:
            print(compare.iloc[n,:])
            dt.append(compare.iloc[n,0])
    return dt
        

def adjustID():
    dt=adjustDate()
    df=pd.read_excel('C:/Users/xiaofeng.li/Downloads/Jan2018.xlsx',header=0)
    df.Date=pd.DatetimeIndex(df.Date).normalize()   
    df=df[(df.Tag=='Bonus Adjustment') | (df.Tag=='Cut Bonus Adjustment')]
    
    df_adjust=pd.read_csv('C:/Users/xiaofeng.li/Downloads/JAN2018_S_ADJUST.csv')
    df_adjust['DT']=pd.to_datetime(df_adjust.DT)
    
    
    
    if len(dt) != 1:
        for n in dt:
            print(n)
            P_id=[]
            S_id=[]
    
            for i in range(0,len(df)):
                if df.iloc[i,8] == n:
                    P_id.append(df.iloc[i,1])
    
                    
            for j in range(0,len(df_adjust)):
                if df_adjust.iloc[j,0] == n:
                    S_id.append(df_adjust.iloc[j,2])
            
            for m in P_id:
                if m not in S_id:
                    print(m,'IN PHILIPPINES REPORT, NOT IN SINGAPORE REPORT')
            
            for k in S_id:
                if k not in P_id:
                    print(k,'IN SINGAPORE REPORT,NOT IN PHILIPPINES REPORT')
    else:
        n = dt
        print(n)
        P_id=[]
        S_id=[]
    
        for i in range(0,len(df)):
            if df.iloc[i,8] == n:
                P_id.append(df.iloc[i,1])
    
                    
        for j in range(0,len(df_adjust)):
            if df_adjust.iloc[j,0] == n:
                S_id.append(df_adjust.iloc[j,2])
            
        for m in P_id:
            if m not in S_id:
                print(m,'IN PHILIPPINES REPORT, NOT IN SINGAPORE REPORT')
            
        for k in S_id:
            if k not in P_id:
                print(k,'IN SINGAPORE REPORT,NOT IN PHILIPPINES REPORT')


adjustID()

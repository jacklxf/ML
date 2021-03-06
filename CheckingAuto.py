import numpy as np
import pandas as pd


def autoDate():
    df=pd.read_excel('C:/Users/xiaofeng.li/Downloads/Jan2018.xlsx',header=0)
    df.Date=pd.DatetimeIndex(df.Date).normalize()
    P_auto_list=[]
    for num in range(1,32):
        amt=round(sum(df['Amount'][(df.Tag == 'Auto Cashin') & (df.Date=='2018-01-%s' %num)])) 
            #print ('Jan%s:' %num, amt)
        P_auto_list.append(amt)
    
    df_auto=pd.read_csv('C:/Users/xiaofeng.li/Downloads/JAN2018_S_AUTO.csv')
    df_auto['DT']=pd.to_datetime(df_auto.DT)
    S_auto_list=[]
    for num in range(1,32):
        amt=round(sum(df_auto['BONUS'][df_auto.DT=='2018-01-%s' %num]))
        S_auto_list.append(amt)
            #S_auto_list.append(amt)

    
    compare=pd.DataFrame(columns=['date','P_auto','S_auto'])
    date=pd.date_range('2018-1-1','2018-1-31')
    compare['date']=date
    compare['P_auto']=P_auto_list
    compare['S_auto']=S_auto_list
    
    dt=[]
    for n in range(0,len(compare)):
        if compare.iloc[n,1] != compare.iloc[n,2]:
            print(compare.iloc[n,:])
            dt.append(compare.iloc[n,0])
    return dt


def autoID():
    dt=autoDate()
    df=pd.read_excel('C:/Users/xiaofeng.li/Downloads/Jan2018.xlsx',header=0)
    df.Date=pd.DatetimeIndex(df.Date).normalize()   
    df=df[df.Tag=='Auto Cashin']
    
    
    df_auto=pd.read_csv('C:/Users/xiaofeng.li/Downloads/JAN2018_S_AUTO.csv')
    df_auto['DT']=pd.to_datetime(df_auto.DT)
    
    if len(dt) != 1:
        for n in dt:
            print(n)
            P_id=[]
            S_id=[]
    
            for i in range(0,len(df)):
                if df.iloc[i,8] == n:
                    P_id.append(df.iloc[i,1])
    
                    
            for j in range(0,len(df_auto)):
                if df_auto.iloc[j,0] == n:
                    S_id.append(df_auto.iloc[j,2])
            
            for m in P_id:
                if m not in S_id:
                    print(m,'IN PHILIPPINES REPORT, NOT IN SINGAPORE REPORT')
            
            for k in S_id:
                if k not in P_id:
                    print(k,'IN SINGAPORE REPORT,NOT IN PHILIPPINES REPORT')
            
    else:
        n=dt
        print(n)
        P_id=[]
        S_id=[]
    
        for i in range(0,len(df)):
            if df.iloc[i,8] in n:
                P_id.append(df.iloc[i,1])
    
                    
        for j in range(0,len(df_auto)):
            if df_auto.iloc[j,0] in n:
                S_id.append(df_auto.iloc[j,2])
            
        for m in P_id:
            if m not in S_id:
                print(m,'IN PHILIPPINES REPORT, NOT IN SINGAPORE REPORT')
            
        for k in S_id:
            if k not in P_id:
                print(k,'IN SINGAPORE REPORT,NOT IN PHILIPPINES REPORT')
        

autoID()                   
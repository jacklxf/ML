import numpy as np
import pandas as pd

def systemDate():
    df = pd.read_excel('C:/Users/xiaofeng.li/Downloads/Jan2018.xlsx', header=0)
    df.Date = pd.DatetimeIndex(df.Date).normalize()
    P_system=[]
    for num in range(1, 32):
        amt = sum(df['Amount'][(df.Tag == 'System Bonus') & (df.Date == '2018-01-%s' % num)]) + sum(
            df['Amount'][(df.Tag == 'Cut System Bonus') & (df.Date == '2018-01-%s' % num)])
        P_system.append(amt)
    
    df_system1=pd.read_csv('C:/Users/xiaofeng.li/Downloads/JAN2018_S_SYSTEMFUNDIN.csv')

    df_system1['DT']=pd.to_datetime(df_system1.DT)
    #print('The month total:',system1_amt)
    S_system1=[]
    for num in range(1,32):
        amt=sum(df_system1['BONUS'][df_system1.DT=='%s-JAN-18' %num])
        S_system1.append(amt)
    
    df_system2=pd.read_csv('C:/Users/xiaofeng.li/Downloads/JAN2018_S_SYSTEMADJUST.csv')

    df_system2['DT']=pd.to_datetime(df_system2.DT)
    #print('The month total:',system2_amt)
    S_system2=[]
    for num in range(1,32):
        amt=sum(df_system2['BONUS'][df_system2.DT=='%s-JAN-18' %num])
        S_system2.append(amt)
    
    
    compare=pd.DataFrame(columns=['date','P_system','S_system1','S_system2'])
    date=pd.date_range('2018-1-1','2018-1-31')
    compare['date']=date
    compare['P_system']=P_system
    compare['S_system1']=S_system1
    compare['S_system2']=S_system2
    
    dt=[]
    for n in range(0,len(compare)):
        if compare.iloc[n,1] != compare.iloc[n,2]+compare.iloc[n,3]:
            print(compare.iloc[n,:])
            dt.append(compare.iloc[n,0])
    return dt


def systemID():
    dt=systemDate()
    df=pd.read_excel('C:/Users/xiaofeng.li/Downloads/Jan2018.xlsx',header=0)
    df.Date=pd.DatetimeIndex(df.Date).normalize()   
    df=df[(df.Tag=='System Bonus') | (df.Tag=='Cut System Bonus')]
    
    df_system1=pd.read_csv('C:/Users/xiaofeng.li/Downloads/JAN2018_S_SYSTEMFUNDIN.csv')
    df_system1['DT']=pd.to_datetime(df_system1.DT)
    df_system1=df_system1[df_system1['BONUS'] !=0]
    df_system1['FCODE']=df_system1['FCODE'].str.slice(0,11)
    df_system2=pd.read_csv('C:/Users/xiaofeng.li/Downloads/JAN2018_S_SYSTEMADJUST.csv')
    df_system2['DT']=pd.to_datetime(df_system2.DT)
    df_system2['FCODE']=df_system2['FCODE'].str.slice(0,9)
    
    
    if len(dt) != 1:
        for n in dt:
            
            print(n)
            P_id=[]
            S_id=[]
    
            for i in range(0,len(df)):
                if df.iloc[i,8] == n:
                    P_id.append(df.iloc[i,1])
    
                    
            for j in range(0,len(df_system1)):
                if df_system1.iloc[j,0] == n:
                    S_id.append(df_system1.iloc[j,2])
            
            for h in range(0,len(df_system2)):
                if df_system2.iloc[h,0] == n:
                    S_id.append(df_system2.iloc[h,2])
            
            
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
    
                    
        for j in range(0,len(df_system1)):
            if df_system1.iloc[j,0] == n:
                S_id.append(df_system1.iloc[j,2])
            
        for h in range(0,len(df_system2)):
            if df_system2.iloc[h,0] == n:
                S_id.append(df_system2.iloc[h,2])
            
            
        for m in P_id:
            if m not in S_id:
                print(m,'IN PHILIPPINES REPORT, NOT IN SINGAPORE REPORT')
            
        for k in S_id:
            if k not in P_id:
                print(k,'IN SINGAPORE REPORT,NOT IN PHILIPPINES REPORT')
                    
systemID()

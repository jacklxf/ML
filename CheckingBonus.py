import numpy as np
import pandas as pd
from difflib import ndiff
#the whole year amount
def P_monthAmt():
    df = pd.read_excel('C:/Users/xiaofeng.li/Downloads/Jan2018.xlsx', header=0)
    system_amount=sum(df['Amount'][(df.Tag=='System Bonus')])+sum(df['Amount'][(df.Tag=='Cut System Bonus')])
    adjustment_amount=sum(df['Amount'][(df.Tag=='Bonus Adjustment')])+sum(df['Amount'][(df.Tag=='Cut Bonus Adjustment')])
    auto_cashin=sum(df['Amount'][(df.Tag=='Auto Cashin')])
    print('System Bonus:', system_amount)
    print('Bonus Adjustment:', adjustment_amount)
    print('Auto Cashin:', auto_cashin)
    

#daily amount for auto-cashin
def P_autoDailyAmt():
    df=pd.read_excel('C:/Users/xiaofeng.li/Downloads/Jan2018.xlsx',header=0)
    df.Date=pd.DatetimeIndex(df.Date).normalize()
    P_auto_list=[]
    for num in range(1,32):
        amt=round(sum(df['Amount'][(df.Tag == 'Auto Cashin') & (df.Date=='2018-01-%s' %num)])) 
        #print ('Jan%s:' %num, amt)
        P_auto_list.append(amt)
    return P_auto_list

def S_df_auto_Amt():
    df_auto=pd.read_csv('C:/Users/xiaofeng.li/Downloads/JAN2018_S_AUTO.csv')
    df_auto['DT']=pd.to_datetime(df_auto.DT)
    #auto_amt=round(sum(df_auto['BONUS']))
    #print('The month total:',auto_amt)
    S_auto_list=[]
    for num in range(1,32):
        amt=round(sum(df_auto['BONUS'][df_auto.DT=='2018-01-%s' %num]))
        #print('Jan%s:' %num, amt)
        S_auto_list.append(amt)
    return S_auto_list


#daily amount for adjust-bonus 
        
def P_adjustDailyAmt():
    df=pd.read_excel('C:/Users/xiaofeng.li/Downloads/Jan2018.xlsx',header=0)
    df.Date=pd.DatetimeIndex(df.Date).normalize()
    for num in range(1,32):
        amt=round(sum(df['Amount'][(df.Tag == 'Bonus Adjustment') & (df.Date=='2018-01-%s' %num)]) + sum(df['Amount'][(df.Tag == 'Cut Bonus Adjustment') & (df.Date=='2018-01-%s' %num)]))
        print ('Jan%s:' %num, amt)
        
def S_df_adjust_Amt():
    df_adjust=pd.read_csv('C:/Users/xiaofeng.li/Downloads/JAN2018_S_ADJUST.csv')
    adjust_amt=sum(df_adjust['BONUS'])
    print('The month total:',adjust_amt)
    for num in range(1,32):
        amt=sum(df_adjust['BONUS'][df_adjust.DT=='%s-JAN-18' %num]) 
        print('Jan%s:' %num, amt)
        
        
#daily amount for system-bonus
        
def P_systemDailyAmt():
    df=pd.read_excel('C:/Users/xiaofeng.li/Downloads/Jan2018.xlsx',header=0)
    df.Date=pd.DatetimeIndex(df.Date).normalize()
    for num in range(1,32):
        amt=sum(df['Amount'][(df.Tag == 'System Bonus') & (df.Date=='2018-01-%s' %num)]) + sum(df['Amount'][(df.Tag == 'Cut System Bonus') & (df.Date=='2018-01-%s' %num)])
        print ('Jan%s:' %num, amt)


def S_df_system1_Amt():
    df_system1=pd.read_csv('C:/Users/xiaofeng.li/Downloads/JAN2018_S_SYSTEMFUNDIN.csv')
    system1_amt=sum(df_system1['BONUS'])
    print('The month total:',system1_amt)
    for num in range(1,32):
        amt=sum(df_system1['BONUS'][df_system1.DT=='%s-JAN-18' %num]) 
        print('Jan%s:' %num, amt)

def S_df_system2_Amt():
    df_system2=pd.read_csv('C:/Users/xiaofeng.li/Downloads/JAN2018_S_SYSTEMADJUST.csv')
    system2_amt=sum(df_system2['BONUS'])
    print('The month total:',system2_amt)
    for num in range(1,32):
        amt=sum(df_system2['BONUS'][df_system2.DT=='%s-JAN-18' %num]) 
        print ('Jan%s:' %num, amt)








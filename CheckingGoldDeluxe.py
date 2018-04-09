# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import pandas as pd

df1=pd.read_excel('/home/lxf/Documents/GDL_201801_daily.xlsx',header=0,sheet_name=1)
df1=df1.drop(['Product','Type','HP'],1)
df1_1=df1[(df1.Date=='01/04/2018')]
df1_1_names=df1_1.groupby('MemberCode').sum().reset_index()
df1_1_names.columns=['PLAYER','TURNOVER','GGR']
#print(df1_1.sum())

df2=pd.read_csv('/home/lxf/Documents/gold.csv')
df2=df2.drop(['FGAMENAME'],1)
df2_1=df2[(df2.DT1=='04-JAN-18')]
df2_1_names=df2_1.groupby('PLAYER').sum().reset_index()

df1player=df1_1_names.values.tolist()
df2player=df2_1_names.values.tolist()

df1list=[]
for n in df1player:
    if n not in df2player:
        df1list.append(n)
print(df1list)
print('In philipean report, not in our report')
        
df2list=[]    
for m in df2player:
    if m not in df1player:
        df2list.append(m)
print(df2list)
print('In our report, not in philipean report')
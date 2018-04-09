import numpy as np
import pandas as pd

class different:
    pass

def __main__():
    pass



def columns():
    data1=pd.read_csv('/home/lxf/Documents/amtlog/amtlog19.csv')
    data2=pd.read_csv('/home/lxf/Documents/endbalance/endbalance19.csv')
    columns1=data1.columns
    columns2=data2.columns
    print("Data1 columns:",columns1)
    print("Data2 columns:",columns2)

    for n in columns1:
        if n not in columns2:
            print(n,'%s is in data1 not in data2' %n)

    for m in columns2:
        if m not in columns1:
            print(m,'%s is in data2 not in data1' %m)

def rows():
    data1=pd.read_csv('/home/lxf/Documents/amtlog.csv')
    data2=pd.read_csv('/home/lxf/Documents/endbalance.csv')
    data2=data2[data2['FAMOUNT']!=0]
    for n in data1.values:
        if n not in data2.values:
            print(n)
    
    for m in data2.values:
        if m not in data1.values:
            print(m)

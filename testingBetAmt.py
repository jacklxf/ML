
import numpy as np
import pandas as pd
import argparse

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('filename',type=str)
    args=parser.parse_args()
    result=sumBetAmt(args.filename)
    print(result)


def sumBetAmt(filename):
    data=pd.read_csv('C:/Users/xiaofeng.li/Downloads/'+filename+'.csv')
    if 'Bet Amount' in data.columns:
        return np.sum(data['Bet Amount'])

    else:
        print('Please collect correct filename')
        
if __name__=="__main__":
    main()








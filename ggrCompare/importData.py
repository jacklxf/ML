import pandas as pd

dt=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20'
    ,'21','22','23','24','25','26','27','28','29','30','31']
ggrfilename='SSS988_GD_AmtLogGGR_201805'
vendorfilename='SSS988_GOLDDELUXE_DAILY_201805'

def ggrImport():
    ggr = pd.DataFrame()
    for day in dt:
        address=ggrfilename+day+'.csv'
        df = pd.read_csv(address)
        df['date']=day
        ggr = pd.concat([ggr, df])
    print('ggr data has imported.')
    return ggr


def vendorImport():
    vendor = pd.DataFrame()
    for day in dt:
        address=vendorfilename+day+'_CNY.csv'
        df = pd.read_csv(address)
        df['date']=day
        vendor = pd.concat([vendor, df])
    print('vendor data has imported.')
    return vendor

import pandas as pd
import numpy as np
import os, sys, errno
import datetime
import argparse
import json
import matplotlib
from matplotlib import pyplot as plt

def create_dirs(directory):
	if not os.path.exists(directory):
		os.makedirs(directory)
#mapping
currency_mapping = {
    "SSS988":['RMB'],
    "SG988": ["RMB", "THB", "VND"],
    "618":["RMB"]
}

amtlog_brand_gamename_mapping ={
    "SSS988":
        ['AsiaGaming','BBIN','EA','GD','GNC','IBC','MGS','PlayTech','Quickfire','Sportbook','SunCasino','TTG','UGS','Stag8','DreamTech','LXV2'],
    "SG988":
        ['AsiaGaming','BBIN','CROWN','EA','GD','PlayTech','SunCasino', 'TTG', 'W88'],
     "618":
         ['AsiaGaming','PlayTech','SunCasino','TTG','UGS','Laxino']
    }

amtlog_vs_vendor_brand_gamename_mapping = {
    "SSS988":{'AsiaGaming':'ASIAGAMING',
              'BBIN':'BBIN',
              'EA':'EA',
              'GD':'GOLDDELUXE',
              'GNC':'GENESIS',
              'HoGaming':'HOGAMING',
              'IBC':'IBC',
              'MGS':'MGSPOKER_CASINOPROFIT',
              'PlayTech':'PLAYTECH',
              'Quickfire':'QUICKFIRE',
              'Sportbook':'SB',
              'SunCasino':'SUNCASINO',
              'TTG':'CHATWELL',
              'UGS':'UGS',
              'Stag8':'STAG8',
              'DreamTech':'DREAMTECH',
              'LXV2':'LAXINOV2'},
    "SG988": {
             'TTG':'CHATWELL',
             'CROWN':'CROWNCASINO',
             'EA':'EA',
             'GD':'GOLDDELUXE',
             'BBIN':'BBIN',
             'SunCasino':'SUNCASINO',
             'PlayTech': 'PLAYTECH',
             'AsiaGaming':'ASIAGAMING',
             'W88':'W88'},
    "618": {'AsiaGaming':'ASIAGAMING',
            'PlayTech':'PLAYTECH',
            'SunCasino':'SUNCASINO',
            'TTG':'CHATWELL',
            'UGS':'UGS',
            'Laxino':'LAXINO'}
}

gamename_vs_jackpot_mapping = {
    "SSS988":{'PlayTech':'PLAYTECH',
              'Quickfire':'QUICKFIRE',
              'UGS':"UGS"}
}
gamename_vs_unsettle_mapping = {
    "SSS988":{'IBC':'IBC',
              'Sportbook':'SB',
              'Stag8':'STAG8'}
}
gamename_vs_missing_mapping = {
    "SSS988":{'Sportbook':'Sportbook' }
}

gamename_vs_lossall_mapping = {
    "SSS988":{'Stag8':'Stag8' }
}
#parameter
parser = argparse.ArgumentParser()
parser.add_argument('--date', required=False, default=None)
parser.add_argument('--base-dir', required=True, default=None)
parser.add_argument('--brand', required=False, default=None)



#time
opts, extOpts = parser.parse_known_args()
date = datetime.datetime.now() + datetime.timedelta(days=-2)
next_date = datetime.datetime.now() + datetime.timedelta(days=-3)
if opts.date:
    date = datetime.datetime.strptime(opts.date, "%Y-%m-%d")
    next_date = date + datetime.timedelta(days=+1)

def daterange(start, stop, step=datetime.timedelta(days=1), inclusive=False):
    if step.days > 0:
        while start < stop:
            yield start
            start = start + step
    elif step.days < 0:
        while start > stop:
            yield start
            start = start + step
    if inclusive and start == stop:
        yield start

def brandConverter(brand):
    if brand.upper() in ["SSS988", "SSS"]:
        return "SSS"
    else:
        return brand.upper()

def currConv(currency):
 if currency.upper() in ['RMB', 'CNY']:
     return 'CNY'
 else:
     return currency.upper()

for brand, currencies in currency_mapping.iteritems():
    if opts.brand and brand != opts.brand:
        continue
    for currency in currencies:
        summary_output_data_final = pd.DataFrame()
        for date in daterange(date.replace(day=1), date+datetime.timedelta(+1)):
            target_date = date.strftime("%Y%m%d")
            target_month = date.strftime("%Y%m")  #convert datetime to string
            keyname_date = date.strftime("%Y-%m-%d")
            nexdate = date+datetime.timedelta(+1)
            target_next_date = nexdate.strftime("%Y%m%d")
            target_month_stag8 = nexdate.strftime("%Y%m")

            columns=['Date','GGR']
            summary_output_data = pd.DataFrame(columns=columns)
            summary_output_data.loc[len(summary_output_data)]=(target_date,'Amt_log')
            summary_output_data.loc[len(summary_output_data)]=(' ' , 'Vendor')
            summary_output_data.loc[len(summary_output_data)]=(' ' , 'Jackpot')
            summary_output_data.loc[len(summary_output_data)]=(' ' , 'Unsettle Bet')
            summary_output_data.loc[len(summary_output_data)] = (' ', 'Missing Debit')
            summary_output_data.loc[len(summary_output_data)] = (' ', 'Loss All')
            summary_output_data.loc[len(summary_output_data)]=(' ', 'Difference')
            summary_output_data.loc[len(summary_output_data)]=(' ', 'Percentage')

            gamenames = amtlog_brand_gamename_mapping[brand]
            for gamename in gamenames:
                amtlog = opts.base_dir +"/OureaDataSummary/" + brand + "/OureaAmountLogGGR/" +target_month+ "/" +brand + "_" +gamename+'_'+ "AmtLogGGR_"+ target_date+".csv"
                if os.path.isfile(amtlog):
                    amtlog1 = pd.read_csv(amtlog,error_bad_lines=False, header=0)
                    amtlog1 = amtlog1.loc[amtlog1["FCURRENCY"] == str(currency).upper()]
                    amtlog2 = amtlog1[["username", "game_name", "FAMOUNT"]].groupby(by=['username']).sum().reset_index()
                    amtlog_sum = amtlog2['FAMOUNT'].sum()

                    for amtgamename, vendorgame in amtlog_vs_vendor_brand_gamename_mapping[brand].iteritems():
                        if amtgamename == gamename:
                            keyname= brand+'#'+keyname_date+'#'+vendorgame+'#'+'Winloss'+'#'+currConv(currency)
                            vendorggr = opts.base_dir + "/" + "LogBasedMonitoring/" + brandConverter(brand) + "/MonthlyWLCompare/" +target_month +"/"+ target_month + '-'+ 'vendordailycompare.json'
                            vendorggr1 = json.loads(open(vendorggr).read())
                            if keyname in vendorggr1:
                                vendorggr_sum= float(vendorggr1.get(keyname)['amountFromVendor'])
                                summary_output_data[gamename] = pd.Series([amtlog_sum, vendorggr_sum])
                                summary_output_data = summary_output_data.fillna(0)

                            if brand in gamename_vs_jackpot_mapping:
                                for jackpot_game, jackpot_name in gamename_vs_jackpot_mapping[brand].iteritems():
                                    if gamename in gamename_vs_jackpot_mapping[brand]:
                                        jackpot_name = gamename_vs_jackpot_mapping[brand][gamename]
                                        if jackpot_name == "UGS":
                                            jackpot = opts.base_dir + "/OureaDataSummary/" + brand + "/VendorDailySummary/UGS/" + target_month + "/" + 'SSS988_UGS_DAILY_JACKPOT_' + target_date + '_CNY.csv'
                                            if os.path.isfile(jackpot):
                                                jackpot1 = pd.read_csv(jackpot, error_bad_lines=False, header=0, usecols=["baseWinAmount"])
                                                totalJackpot = jackpot1["baseWinAmount"].sum()
                                                summary_output_data.loc[2, ['UGS']] = -totalJackpot
                                        elif jackpot_name == 'PLAYTECH':
                                            jackpot = opts.base_dir +"/OureaDataSummary/" + brand + "/VendorDailySummary/PLAYTECH/" + target_month+ "/"+ 'SSS988_PLAYTECH_DAILY_' + target_date + '_CNY.csv'
                                            if os.path.isfile(jackpot):
                                                jackpot1 = pd.read_csv(jackpot, error_bad_lines=False, header=0,skiprows=[0], usecols=["Progressive Win"])
                                                totalJackpot = jackpot1["Progressive Win"].sum()
                                                summary_output_data.loc[2,['PlayTech']]= totalJackpot
                                        elif jackpot_name == "QUICKFIRE":
                                            jackpot = opts.base_dir +"/OureaDataSummary/" + brand + "/VendorDailySummary/QUICKFIRE/" + target_month + "/" + 'SSS988_QUICKFIRE_DAILY_JACKPOT_' + target_date + '_CNY.csv'
                                            if os.path.isfile(jackpot):
                                                jackpot1 = pd.read_csv(jackpot, error_bad_lines=False, header=0, usecols=["JackPotWinAmount"])
                                                totalJackpot = jackpot1["JackPotWinAmount"].sum()
                                                summary_output_data.loc[2, ['Quickfire']] = totalJackpot

                                for unsettle_game, unsettle_name in gamename_vs_unsettle_mapping[brand].iteritems():
                                    if gamename in gamename_vs_unsettle_mapping[brand]:
                                        unsettle_name = gamename_vs_unsettle_mapping[brand][gamename]

                                        if unsettle_name == 'SB':
                                            unsettle = opts.base_dir + "/OureaDataSummary/" + brand + "/VendorDailySummary/SB/" + target_month + "/" + 'SSS988_SB_UNSETTLED-DAILY_UNSETTLED_' + target_date + '_CNY.csv'
                                            if os.path.isfile(unsettle):
                                                unsettle1 = pd.read_csv(unsettle, error_bad_lines=False, header=0)
                                                unsettle1 = pd.Series(unsettle1["Member Exposure"])
                                                unsettle1 = pd.to_numeric(unsettle1,errors='coerce').fillna(0)
                                                #totalunsettle = pd.Series(unsettle1["Member Exposure"]).convert_objects(convert_numeric=True)
                                                totalunsettle = unsettle1.sum()
                                                summary_output_data.loc[3, ['Sportbook']] = totalunsettle
                                            else:
                                                summary_output_data.loc[3, ['Sportbook']] = 0

                                        if unsettle_name == 'IBC':
                                            unsettle_ibc = opts.base_dir + "/OureaDataSummary/" + brand + "/VendorDailySummary/IBC/" + target_month + "/" + 'SSS988_IBC_UNSETTLED-DAILY_UNSETTLED_' + target_date + '_CNY.csv'
                                            if os.path.isfile(unsettle_ibc):
                                                unsettle1_ibc = pd.read_csv(unsettle_ibc, header=0)
                                                summary_output_data.loc[3, ['IBC']] = pd.to_numeric(list(
                                                    map(lambda y: y.replace(",", ""), unsettle1_ibc["Stake"]))).sum()
                                            else:
                                                summary_output_data.loc[3, ['IBC']] = 0

                                        if unsettle_name == 'STAG8':
                                            unsettle = opts.base_dir + "/OureaDataSummary/" + brand + "/VendorDailySummary/STAG8/" + target_month_stag8 + "/" + 'SSS988_STAG8_UNSETTLED-DAILY_UNSETTLED_' + target_next_date + '_CNY.csv'
                                            if os.path.isfile(unsettle):
                                                unsettle1 = pd.read_csv(unsettle, error_bad_lines=False, header=0)
                                                summary_output_data.loc[3, ['Stag8']] = unsettle1["Stake"].sum()
                                            else:
                                                summary_output_data.loc[3, ['Stag8']] = 0

                                for missing_game, missing_name in gamename_vs_missing_mapping[brand].iteritems():
                                    if gamename in gamename_vs_missing_mapping[brand]:
                                        missing_name = gamename_vs_missing_mapping[brand][gamename]
                                        if missing_name == 'Sportbook':
                                            path = opts.base_dir + "/OureaDataSummary/" + brand + "/OureaAmountLogGGR/" + target_month + "/" + "SSS988_Sportbook_AmtLogGGR_" + target_date + ".csv"
                                            if os.path.isfile(path):
                                                missing_sb = pd.read_csv(path, error_bad_lines=False, header=None)
                                                v = path.split("_")
                                                g = v[-1].split(".")
                                                fdate = datetime.datetime.strptime(g[0], '%Y%m%d')
                                                dateString = fdate.strftime('%Y%m%d')
                                                dateStringList = []
                                                single_credit_transaction = []
                                                for x in range(0, 11):
                                                    dateStringList.append(
                                                        (fdate - datetime.timedelta(days=x)).strftime('%Y%m%d'))

                                                if os.path.isfile(path) == True:
                                                    f = pd.read_csv(path, error_bad_lines=False, header=None)

                                                    all_Transaction = []
                                                    debit_Transaction = []

                                                    all_Transaction = f.values.tolist()

                                                    for row1 in all_Transaction:
                                                        if row1[1] == 'Debit':
                                                            debit_Transaction.append(row1[0])

                                                    for row2 in all_Transaction:
                                                        if row2[0] not in debit_Transaction:
                                                            single_credit_transaction.append(row2)

                                                all_debit_Transaction_full = []
                                                for fdate in dateStringList:
                                                    filePath2 = opts.base_dir + "/OureaDataSummary/" + brand + "/OureaAmountLogGGR/" + target_month + "/" + "SSS988_Sportbook_AmtLogGGR_" + fdate + '.csv'
                                                    if os.path.isfile(filePath2) == True:
                                                        f2 = pd.read_csv(filePath2, error_bad_lines=False, header=None)
                                                        temp_Transaction = []
                                                        temp_Transaction = f2.values.tolist()
                                                        for row3 in temp_Transaction:
                                                            if row3[1] == 'Debit':
                                                                all_debit_Transaction_full.append(row3)

                                                full_debit_credit_transaction = []
                                                for row5 in single_credit_transaction:
                                                    results = [debit for debit in all_debit_Transaction_full if
                                                               debit[0] == row5[0]]
                                                    if results:
                                                        full_debit_credit_transaction.append(results[0])

                                                if len(full_debit_credit_transaction) > 0:
                                                    full_debit_credit_transaction.pop(0)
                                                df = pd.DataFrame(full_debit_credit_transaction,
                                                                  columns=["FTRANSID", "FTRANSTYPE", "FWALLETTYPE",
                                                                           "username", "game_name", "FAMOUNT",
                                                                           "FAMTBEFOREOP", "FAMTAFTEROP", "fdate",
                                                                           "FDESC", "FOPERATORNAME", "FHOUSEPLAYER",
                                                                           "FCURRENCY", "FWEBCODE"])
                                                df_sum = pd.to_numeric(df['FAMOUNT']).sum()
                                                if df_sum !=0:
                                                    summary_output_data.loc[4, ['Sportbook']] = df_sum.astype(float)

                                for loseall_game, lossall_name in gamename_vs_lossall_mapping[brand].iteritems():
                                    if gamename in gamename_vs_lossall_mapping[brand]:
                                        loseall_game = gamename_vs_lossall_mapping[brand][gamename]
                                        if loseall_game == 'Stag8':
                                            lossall = opts.base_dir + "/OureaDataSummary/" + brand + "/VendorDailySummary/STAG8/" + target_month + "/" + 'SSS988_STAG8_DAILY_' + target_date + '_CNY.csv'
                                            lossall_stag8 = pd.read_csv(lossall, header=0)
                                            lossall_stag8 = lossall_stag8["LoseAll"].sum()
                                            summary_output_data.loc[5, ['Stag8']] = lossall_stag8
                                        else:
                                            summary_output_data.loc[5, ['Stag8']] = 0


                        summary_output_data.iloc[6, 2:] = (summary_output_data.iloc[0, 2:]+ summary_output_data.iloc[4, 2:]+summary_output_data.iloc[5, 2:]).abs() - (summary_output_data.iloc[1, 2:] + summary_output_data.iloc[2, 2:] + summary_output_data.iloc[3,
                                                                                            2:]).abs()
                        summary_output_data.iloc[7, 2:] = summary_output_data.iloc[6,2:].div((summary_output_data.iloc[0,2:]+summary_output_data.iloc[4, 2:]+summary_output_data.iloc[5, 2:]).replace(0, np.nan))

                        summary_output_data.iloc[7,2:] =(summary_output_data.iloc[7,2:]).abs()*100

                        summary_output_data = np.round(summary_output_data,decimals=2)
                        summary_output_data.iloc[7,2:] = summary_output_data.iloc[7,2:].astype(float).map('{:,.2f}%'.format)

            summary_output_data_final = summary_output_data_final.append(summary_output_data)
            summary_output_data_final = summary_output_data_final.fillna(0)
            summary_output_data_final.set_index(["Date", "GGR"], inplace=True)
            summary_output_data_final = summary_output_data_final.reset_index()

        a = summary_output_data_final.loc[summary_output_data_final['GGR'] == 'Amt_log']
        b = summary_output_data_final.loc[summary_output_data_final['GGR'] == 'Vendor']
        c = summary_output_data_final.loc[summary_output_data_final['GGR'] == 'Jackpot']
        d = summary_output_data_final.loc[summary_output_data_final['GGR'] == 'Unsettle Bet']
        g = summary_output_data_final.loc[summary_output_data_final['GGR'] == 'Missing Debit']
        h = summary_output_data_final.loc[summary_output_data_final['GGR'] == 'Loss All']
        e = summary_output_data_final.loc[summary_output_data_final['GGR'] == 'Difference']
        f = summary_output_data_final.loc[summary_output_data_final['GGR'] == 'Percentage']

        a1 = a.ix[:,2:].sum()
        b1 = b.ix[:,2:].sum()
        c1 = c.ix[:,2:].sum()
        d1 = d.ix[:,2:].sum()
        e1 = e.ix[:,2:].sum()
        g1 = g.ix[:,2:].sum()
        h1 = h.ix[:,2:].sum()
        f1 = (a1+ g1+h1).abs() - (b1 + c1 + d1).abs()
        f10 = f1/(a1+ g1+h1).abs()*100
        f11= f10.astype(float).map('{:,.2f}%'.format)

        a2 = pd.Series(['Total','Amt_log'],index=['Date','GGR'] )
        b2 = pd.Series([' ','Vendor'],index=['Date','GGR'] )
        c2 = pd.Series([' ','Jackpot'],index=['Date','GGR'] )
        d2 = pd.Series([' ','Unsettle Bet'],index=['Date','GGR'] )
        g2 = pd.Series([' ', 'Missing Debit'], index=['Date', 'GGR'])
        h2 = pd.Series([' ', 'Loss All'], index=['Date', 'GGR'])
        e2 = pd.Series([' ','Difference'],index=['Date','GGR'] )
        f2 = pd.Series([' ','Percentage'],index=['Date','GGR'] )

        a3= a2.append(a1)
        b3= b2.append(b1)
        c3= c2.append(c1)
        d3= d2.append(d1)
        g3= g2.append(g1)
        h3 = h2.append(h1)
        e3= e2.append(e1)
        f3=f2.append(f11)

        gamelist = []
        if brand == 'SSS988':
            gamelist = ['', '', 'AsiaGaming', 'BBIN', 'EA', 'GD', 'GNC', 'IBC','MGS', 'PlayTech','Quickfire','Sportbook','SunCasino','TTG','UGS','Stag8','DreamTech', 'LXV2']
        if brand == 'SG988':
            gamelist = ['','','TTG','CROWN','EA','GD','BBIN','SunCasino','PlayTech','AsiaGaming','W88']
        if brand == "618":
            gamelist = ['','','AsiaGaming','PlayTech','SunCasino','TTG','UGS','Laxino']

        summary_output_data_final.loc[len(summary_output_data_final)] = gamelist
        summary_output_data_final = summary_output_data_final.append(a3,ignore_index=True)
        summary_output_data_final = summary_output_data_final.append(b3,ignore_index=True)
        summary_output_data_final = summary_output_data_final.append(c3,ignore_index=True)
        summary_output_data_final = summary_output_data_final.append(d3,ignore_index=True)
        summary_output_data_final = summary_output_data_final.append(g3,ignore_index=True)
        summary_output_data_final = summary_output_data_final.append(h3,ignore_index=True)
        summary_output_data_final = summary_output_data_final.append(e3,ignore_index=True)
        summary_output_data_final = summary_output_data_final.append(f3,ignore_index=True)

        #print(summary_output_data_final)
        #summary_output_data_final.to_excel('output.xlsx', index=False, header=True)

        target_dir = opts.base_dir + "/OureaDataSummary/" + brand+ "/AmounLog_vs_VendorGGR"
        create_dirs(target_dir)
        target_file = target_dir + '/' + brand + '_AmounLog_vs_VendorGGR_' + target_month + "_" + currency + '.xlsx'
        summary_output_data_final.to_excel(target_file, index=False, header=True)

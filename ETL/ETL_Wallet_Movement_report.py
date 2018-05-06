import pymssql
import cx_Oracle
import sys
import json

def main():
    etl(Oracle_extract,datawarehouse_db_config,dsn_tns,sqlserver_insert)

#Database

datawarehouse_name = 'AnalysisRpt'
# Oracle (source db)

ip='10.20.70.195'
port=1521
SID='SUNGAME'
dsn_tns=cx_Oracle.makedsn(ip,port,SID)


# Sql-server (Warehouse db)
datawarehouse_db_config = {
    'server':'SGSSRS01',
    'user':'xiaofeng',
    'password':'Aft123456A'
}

#Sql code
Oracle_extract = ("""
select 
"FGAMENAME",
"FWEBCODE",
"FCURRENCY",
"FDATE",
coalesce(sum("'Deposit'_AMOUNT"),0) "'Deposit'",
coalesce(sum("'Withdraw'_AMOUNT"),0) "'Withdraw'",
coalesce(sum("'Fundin'_AMOUNT"),0) "'Fundin'",
coalesce(sum("'Fundout'_AMOUNT"),0) "'Fundout'",
coalesce(sum( "'Adjustment'_AMOUNT"),0) "'Adjustment'",
coalesce(sum("'Bonus'_AMOUNT"),0) "'Bonus'",
coalesce(sum("'Debit'_AMOUNT"),0) "'Debit'",
coalesce(sum("'Credit'_AMOUNT"),0) "'Credit'",
coalesce(sum("'CancelBet'_AMOUNT"),0) "'CancelBet'",
coalesce(sum("'Refund'_AMOUNT"),0) "'Refund'",
coalesce(sum("'FortuneWheel'_AMOUNT"),0) "'FortuneWheel'",
coalesce(sum("'SyncBalance'_AMOUNT"),0) "'SyncBalance'",
coalesce(sum("'Rebate'_AMOUNT"),0) "'Rebate'",
coalesce(sum("'Tip'_AMOUNT"),0) "'Tip'"
from 
(
select u.fwebcode,u.fcurrency,trunc(amt.fdate) as fdate,g.fgamename,amt.ftranstype,amt.famount
from v_USER_AMOUNTLOG amt 
inner join user_player u 
on amt.fuserid=u.fid 
left join
(
select fgameid,fgamename 
from game_list 
union
select 0, translate('Main Balance' using nchar_cs) as fgamename from dual
) g 
on amt.fgameid=g.fgameid
where 
--amt.fdate>=trunc(sysdate)-1
--and amt.fdate< trunc(sysdate)
u.fhouseplayer='N'
)
pivot
(
sum(famount) amount
for ftranstype in ('Deposit','Withdraw','Fundin','Fundout','Adjustment','Bonus','Debit','Credit','CancelBet','Refund',
'FortuneWheel','SyncBalance','Rebate','Tip')
)
group by "FGAMENAME","FWEBCODE","FCURRENCY","FDATE"
""")

sqlserver_insert = ("""
    INSERT INTO dbo.Wallet_Movement_Summary_report(FGAMENAME,FWEBCODE,FCURRENCY,FDATE,FDEPOSIT,FWITHDRAW,FFUNDIN,FFUNDOUT,FADJUSTMENT,FBONUS,FDEBIT,FCREDIT,FCANCELBET,FREFUND,FFORTUNEWHEEL,FSYNCBALANCE,FREBATE,FTIP)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
""")



#Extraction and Load
def etl(Oracle_extract,datawarehouse_db_config,dsn_tns,sqlserver_insert):

    # extract data from source db
    Oracle_con = cx_Oracle.connect('ssrs_usr','ssrs_usr',dsn_tns)
    cur = Oracle_con.cursor()
    cur.execute(Oracle_extract)
    res = cur.fetchall()
    cur.close()
    Oracle_con.close()

    # load data into warehouse db

    target_cnx = pymssql.connect(**datawarehouse_db_config)
    target_cursor = target_cnx.cursor()
    target_cursor.execute("USE {}".format(datawarehouse_name))
    target_cursor.executemany(sqlserver_insert, res)
    target_cnx.commit()
    print('data loaded to warehouse db')
    target_cursor.close()
    target_cnx.close()

if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'xiaofeng'
import pymssql
import cx_Oracle
import sys
from libtaskpy import taskargs

args = taskargs.TaskArgs()
config = args.config
oracleConfig=config["oracleConfig"]

print("Date From: {} To: {}".format(args.date_from(), args.date_to()))

dsn_tns=cx_Oracle.makedsn(oracleConfig['ip'], oracleConfig['port'], oracleConfig['SID'])

# Sql-server (Warehouse db)
datawarehouse_db_config=config["mssqlServerConfig"]

#Sql code
Oracle_extract = ("""
select 
dm.dt as fdateapproved,
dm.fwebcode,
dm.fcurrency,
coalesce(deposit.actual_amount,0) as factual_amount,
coalesce(withdrawal.withdrawal_amount,0) as fwithdrawal_amount

from 
( select d.dt, brand.fwebcode,brand.fcurrency
from ( select column_value dt from table(get_days_Between(DATE'{}', DATE '{}')) ) d
cross join (
  select * from V_CURRENCY_WEBCODE
) brand )  dm

left join
(
 select trunc(d.fdateapproved) as dt1,sum(decode(d.Fdeposittype,0,d.famount,od.factualamt)) as actual_amount, d.fcurrency,d.fwebcode
from user_deposit d
left join OFFLINE_DEPOSIT od on od.fid=d.fodid
left join user_player p on d.fuserid=p.fid

where 
(d.fdateapproved>= DATE '{}' or DATE '{}' is null)
and (d.fdateapproved< DATE '{}'+1 or DATE '{}' is null)
and d.fstate='1'
and p.fhouseplayer='N'
group by trunc(d.fdateapproved),d.fwebcode,d.fcurrency
) deposit
on dm.dt=deposit.dt1 and dm.fwebcode=deposit.fwebcode and dm.fcurrency=deposit.fcurrency 

left join 
(
select sum(w.famount) as withdrawal_amount,trunc(w.fdateapproved) as dt2,w.fcurrency, w.fwebcode
from user_withdrawal w
left join user_player p on w.fuserid=p.fid
where 
(w.fdateapproved>= DATE '{}' or DATE '{}' is null)
and (w.fdateapproved< DATE '{}'+1 or DATE '{}' is null)
and w.fstatus='4'
and p.fhouseplayer='N'
group by trunc(w.fdateapproved),w.fwebcode,w.fcurrency
) withdrawal
on dm.dt=withdrawal.dt2 and dm.fwebcode=withdrawal.fwebcode and dm.fcurrency=withdrawal.fcurrency 
""".format(args.date_from(), args.date_to(),args.date_from(),args.date_from(), args.date_to(), args.date_to(),args.date_from(),args.date_from(), args.date_to(), args.date_to()))

sqlserver_check=("""
delete from dbo.Deposit_Withdrawal_Summary_report where FDATEAPPROVED='{}' and FDATEAPPROVED<'{}'
""".format(args.date_from(), args.date_to_next_day()))

sqlserver_insert = ("""
    INSERT INTO Deposit_Withdrawal_Summary_report (FDATEAPPROVED,FWEBCODE,FCURRENCY,FACTUAL_AMOUNT,FWITHDRAWAL_AMOUNT)   
    VALUES (%s,%s,%s,%s,%s)  
""")


#Database
datawarehouse_name = 'AnalysisRpt'

#Extraction and Load


# extract data from source db
Oracle_con = cx_Oracle.connect(oracleConfig["user"],oracleConfig["password"],dsn_tns)
print("Oracle connected.")
cur = Oracle_con.cursor()
print("ORA Exec SQL: " + Oracle_extract)
cur.execute(Oracle_extract)
res = cur.fetchall()
cur.close()
Oracle_con.close()
print("Oracle fetch done")

# load data into warehouse db
target_cnx = pymssql.connect(**datawarehouse_db_config)
print("MSSQL connected")
target_cursor = target_cnx.cursor()
target_cursor.execute("USE {}".format(datawarehouse_name))
print("MSSQL Exec SQL: " + sqlserver_check)
target_cursor.execute(sqlserver_check)
print("MSSQL Exec SQL: " + sqlserver_insert)
target_cursor.executemany(sqlserver_insert, res)
target_cnx.commit()
print('Data loaded to warehouse done.')
target_cursor.close()
target_cnx.close()

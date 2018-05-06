import pymssql
import cx_Oracle

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

Oracle_extract = ("""
select
datebet as fdatebet,
fwebcode,
fcurrency,
games as fgames,
cat as fcat,
turnover_cat as fturnover_cat,
ggr_cat as fggr_cat
from
(
	select r.fdatebet as datebet,r.fwebcode,r.fcurrency, g.fgamename as games, 'Total' as cat,sum(r.fbetamt) as turnover_cat, -sum(r.fwinamt) as ggr_cat
	from user_dailyreport r
	left join game_list g
	on g.fgameid=r.fgameid
	where r.fdatebet >=trunc(sysdate)-1
	and r.fdatebet<trunc(sysdate)
	and r.fgameid not in (2,6,8,12,27)
	and r.fhouseplayer='N'
	group by r.fdatebet,r.fwebcode,r.fcurrency,g.fgamename

	union all

	select c.fdatebet as datebet,c.fwebcode,c.fcurrency,g.fgamename as games,coalesce( c.fcategory, 'Total') as cat,sum(c.fbetamt) as turnover_cat, -sum(c.fwinamt) as ggr_cat
	 from user_dailyreport_cat c
	 left join game_list g
	on g.fgameid=c.fgameid
	where
	c.fhouseplayer='N'
	--and c.fdatebet>=trunc(sysdate)-1
	--and c.fdatebet<trunc(sysdate)
	and c.fgameid in (2,6,8,12,27)
    group by grouping sets( (  c.fdatebet,c.fwebcode,c.fcurrency,g.fgamename ,c.fcategory),  (  c.fdatebet,g.fgamename ))
)""")

sqlserver_insert = ("""
    INSERT INTO Turnover_GGR_Cat_report (FDATEBET,FWEBCODE,FCURRENCY,FGAMENAME,FCATEGORY,FTURNOVER_CAT,FGGR_CAT)
    VALUES (%s,%s,%s,%s,%s,%s,%s)
""")

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
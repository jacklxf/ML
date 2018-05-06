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

#Sql code
Oracle_extract = ("""
    select r.fdatebet as datebet,g.fgamename, sum(fbetamt) turnover, -sum(fwinamt) ggr,r.FWEBCODE,r.FCURRENCY
    from user_dailyreport r 
    join game_list g 
    on r.fgameid = g.fgameid
    left join user_player u
    on u.FID=r.FUSERID
    --where fdatebet=trunc(sysdate)-1
    group by r.fdatebet,g.fgamename,r.FWEBCODE,r.FCURRENCY
    order by 1,2
""")

sqlserver_insert = ("""
    INSERT INTO Turnover_GGR_report (FDATEBET,FGAMENAME,FTURNOVER,FGGR)   
    VALUES (%s,%s,%s,%s)  
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

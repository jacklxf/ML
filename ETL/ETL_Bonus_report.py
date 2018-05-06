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
select
auto.dt_auto,
auto.fwebcode,
auto.fcurrency,
auto.auto_cashin_bonus,
adjustment.adjustment_bonus,
system.system_bonus,
adjust_rebate.adj_rebate,
system_rebate.sys_rebate,
jackpot.jackpot_bonus

from 
(
select adj.FDATEACCEPTED as dt_auto,player.FWEBCODE,player.fcurrency,sum(adj_detl.famount) as auto_cashin_bonus
from hplayer_adjustment adj
inner join user_player player
on player.fid = adj.fplayerid
INNER JOIN hplayer_adjustment_detail adj_detl
on adj.fid = adj_detl.fid
where
   player.fhouseplayer = 'N'
   --and adj.FDATEACCEPTED>=trunc(sysdate)-1
   --and adj.FDATEACCEPTED<trunc(sysdate)
   and adj.ftype in ('92')
   and adj.fsubtype in ('155')
group by adj.FDATEACCEPTED,player.FWEBCODE,player.fcurrency
) auto

left join 
(
select player.FWEBCODE,player.FCURRENCY,adj.FDATEACCEPTED as dt_adj, sum(adj_detl.famount) as adjustment_bonus
from hplayer_adjustment adj
inner join user_player player
on player.fid = adj.fplayerid
INNER JOIN hplayer_adjustment_detail adj_detl
on adj.fid = adj_detl.fid
 where  
   player.fhouseplayer = 'N'
   --and adj.FDATEACCEPTED>= trunc(sysdate)-1
   --and adj.FDATEACCEPTED<trunc(sysdate)
   AND adj.ftype  in ('92')
   and adj.fsubtype in ('151','132')
group by adj.FDATEACCEPTED,player.FWEBCODE,player.FCURRENCY
) adjustment
on (auto.dt_auto=adjustment.dt_adj and auto.fwebcode=adjustment.fwebcode and auto.fcurrency=adjustment.fcurrency)

left join
(
select u.fwebcode,u.fcurrency,b.FDATETRANSACTION as dt_sb,  coalesce( sum(b.fbonus),0)  system_bonus
from BONUS_FUNDIN b join user_player u 
on b.fid = u.fid 
where 
	u.fhouseplayer = 'N'
	--and b.FDATETRANSACTION>=trunc(sysdate)-1
	--and b.FDATETRANSACTION<trunc(sysdate)
group by b.FDATETRANSACTION,u.fwebcode,u.fcurrency

union 

select player.fwebcode,player.fcurrency,adj.FDATEACCEPTED as dt_sb, sum(adj_detl.famount) as system_bonus
from hplayer_adjustment adj
inner join user_player player
on player.fid = adj.fplayerid
INNER JOIN hplayer_adjustment_detail adj_detl
on adj.fid = adj_detl.fid
where 
	player.fhouseplayer = 'N'
	--and adj.FDATEACCEPTED>=trunc(sysdate)-1
	--and adj.FDATEACCEPTED<trunc(sysdate)
	AND adj.ftype in ('92')
	and adj.fsubtype in ('156','105','111','117')
	group by adj.FDATEACCEPTED,player.fwebcode,player.fcurrency
) system	
on (auto.dt_auto=system.dt_sb and auto.fwebcode=system.fwebcode and auto.fcurrency=system.fcurrency)

left join
(
select player.fwebcode,player.fcurrency,adj.FDATEACCEPTED as dt, sum(adj_detl.famount) as adj_rebate
from hplayer_adjustment adj
inner join user_player player
on player.fid = adj.fplayerid
INNER JOIN hplayer_adjustment_detail adj_detl
on adj.fid = adj_detl.fid
where adj.fstatus = 'Accepted'
   --and adj.FDATEACCEPTED >=trunc(sysdate)-1
   --and adj.FDATEACCEPTED<trunc(sysdate)   
   AND adj.ftype  in ('91')
   and adj.fsubtype in ('130','103')
   and not exists ( select 1 from user_house h where h.fid = player.fid)
   group by adj.FDATEACCEPTED,player.fwebcode,player.fcurrency
)adjust_rebate
on (auto.dt_auto=adjust_rebate.dt and auto.fwebcode=adjust_rebate.fwebcode and auto.fcurrency=adjust_rebate.fcurrency)


left join 
(	
select t3.fwebcode,t3.fcurrency,t2.FAPPORVEDATE as dt, sum(t2.factamount) sys_rebate
from user_rebate_record t2
inner join user_player t3
on t3.fid = t2.fuserid
  left join CMS_PROMOTION p on t2.FPROMOTIONID = p.fid
     where t2.fstatus = 3
        --and t2.FAPPORVEDATE >= trunc(sysdate)-1
        --and t2.FAPPORVEDATE <trunc(sysdate)   
        and not exists ( select 1 from user_house h where h.fid = t3.fid)
group by t2.FAPPORVEDATE,t3.fwebcode,t3.fcurrency
) system_rebate
on (auto.dt_auto=system_rebate.dt and auto.fwebcode=system_rebate.fwebcode and auto.fcurrency=system_rebate.fcurrency)

left join 
(
select player.fwebcode,player.fcurrency,adj.FDATEACCEPTED as dt_jp, sum(adj_detl.famount) as jackpot_bonus
from hplayer_adjustment adj
inner join user_player player
on player.fid = adj.fplayerid
INNER JOIN hplayer_adjustment_detail adj_detl
on adj.fid = adj_detl.fid
where 
player.fhouseplayer = 'N'
--and adj.FDATEACCEPTED>= trunc(sysdate)-1
--and adj.FDATEACCEPTED <trunc(sysdate)
and adj.ftype in ('92')
and adj.fsubtype in ('131','124','174') 
and player.fhouseplayer = 'N'
group by adj.FDATEACCEPTED,player.fwebcode,player.fcurrency
) jackpot
on (auto.dt_auto=jackpot.dt_jp and auto.fwebcode=jackpot.fwebcode and auto.fcurrency=jackpot.fcurrency)
""")

sqlserver_insert = ("""
    INSERT INTO Bonus_report (FDATE,FWEBCODE,FCURRENCY,FAUTO_CASHIN_BONUS,FSYSTEM_BONUS,FADJ_REBATE,FSYS_REBATE,FJACKPOT)   
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)  
""")


#Extraction and Load
def etl(Oracle_extract,datawarehouse_db_config,dsn_tns,sqlserver_insert):
    # extract data from source db
    Oracle_con = cx_Oracle.connect('ssrs_usr','ssrs_usr',dsn_tns)
    print('Oracle connect done.')
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

import cx_Oracle

ip = '10.20.70.195'
port = 1521
SID = 'SUNGAME'
dsn_tns = cx_Oracle.makedsn(ip, port, SID)


con=cx_Oracle.connect('ssrs_usr','ssrs_usr',dsn_tns)
ver=con.version.split(".")
print(ver)
cur=con.cursor()
cur.execute('select * from user_player')
for result in cur:
	print(result)

cur.close()
con.close()
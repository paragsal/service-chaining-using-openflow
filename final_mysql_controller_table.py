#!/usr/bin/python

import MySQLdb
import socket, struct
# Open database connection

#db = MySQLdb.connect("localhost","testuser","test623","testdb1" )

db = MySQLdb.connect(host="localhost",user="root",passwd="root")
db1 = db.cursor()
db1.execute('CREATE DATABASE test2')
db1.execute("USE test2");


# prepare a cursor object using cursor() method
cursor = db.cursor()

# Drop table if it already exist using execute() method.
#cursor.execute("DROP TABLE IF EXISTS SWITCH1")

# Create table as per requirement
'''
sql = """CREATE TABLE CONTROLLER2 (
         SERVICE  VARCHAR(80) NOT NULL UNIQUE,
         PROVIDER VARCHAR(80),SWITCH VARCHAR(80),PORT VARCHAR(80))"""
'''
#cursor.execute(sql)

cursor.execute("CREATE TABLE CONTROLLER2 (SERVICE VARCHAR(80) NOT NULL UNIQUE, PROVIDER VARCHAR(80),SWITCH VARCHAR(80),OUTPORT VARCHAR(80),INPORT VARCHAR(80),PROVIDER_MAC varchar(80))")
#y='10.0.0.2'

#cursor.execute("ALTER TABLE CONTROLLER ADD COLUMN PORT VARCHAR(40)");
#10.0.0.6 is Srvc1 <-> SW5 -- F1
#
cursor.execute("INSERT INTO CONTROLLER2(SERVICE,PROVIDER,SWITCH,OUTPORT,INPORT,PROVIDER_MAC) VALUES('F1','11.0.1.4,10.0.0.6','4,2','1,1','2,5','2e:43:53:e1:1d:e6')")
 
cursor.execute("INSERT INTO CONTROLLER2(SERVICE,PROVIDER,SWITCH,OUTPORT,INPORT,PROVIDER_MAC) VALUES('TC','10.0.0.3','4','2','2','2e:43:53:e1:1d:e6')")

#cursor.execute("INSERT INTO CONTROLLER2(SERVICE,PROVIDER,SWITCH,OUTPORT,INPORT) VALUES('F2','10.0.0.4','5','3','4')")
db.commit()
# disconnect from server
db.close()

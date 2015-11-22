#!/usr/bin/python

import MySQLdb
import socket, struct
# Open database connection

#db = MySQLdb.connect("localhost","testuser","test623","testdb1" )

db = MySQLdb.connect(host="localhost",user="root",passwd="root")
db1 = db.cursor()
#db1.execute('CREATE DATABASE test1')
db1.execute("USE test1");


# prepare a cursor object using cursor() method
cursor = db.cursor()

# Drop table if it already exist using execute() method.
#cursor.execute("DROP TABLE IF EXISTS SWITCH1")

# Create table as per requirement
'''
sql = """CREATE TABLE CONTROLLER1 (
         SERVICE  VARCHAR(80) NOT NULL UNIQUE,
         PROVIDER VARCHAR(80),SWITCH VARCHAR(80),PORT VARCHAR(80))"""
'''
#cursor.execute(sql)

cursor.execute("CREATE TABLE CONTROLLER1 (SERVICE VARCHAR(80) NOT NULL UNIQUE, PROVIDER VARCHAR(80),SWITCH VARCHAR(80),PORT VARCHAR(80))");
#y='10.0.0.2'

#cursor.execute("ALTER TABLE CONTROLLER ADD COLUMN PORT VARCHAR(40)");

cursor.execute("INSERT INTO CONTROLLER1(SERVICE,PROVIDER,SWITCH,PORT) VALUES('EC','10.0.0.3','4','2')")

cursor.execute("INSERT INTO CONTROLLER1(SERVICE,PROVIDER,SWITCH,PORT) VALUES('ED','10.0.0.4','5','3')")
cursor.execute("INSERT INTO CONTROLLER1(SERVICE,PROVIDER,SWITCH,PORT) VALUES('EA','10.0.0.6,10.0.0.5','3','3')")

cursor.execute("INSERT INTO CONTROLLER1(SERVICE,PROVIDER,SWITCH,PORT) VALUES('EB','10.0.1.1','4,3','3')")
db.commit()
# disconnect from server
db.close()

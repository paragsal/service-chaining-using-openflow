#!/usr/bin/python

import MySQLdb
import socket, struct
# Open database connection

db = MySQLdb.connect("localhost","testuser","test623","testdb1" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Drop table if it already exist using execute() method.
#cursor.execute("DROP TABLE IF EXISTS SWITCH1")

# Create table as per requirement
sql = """CREATE TABLE CONTROLLER (
         SERVICE  VARCHAR(80) NOT NULL UNIQUE,
         PROVIDER VARCHAR(80),SWITCH VARCHAR(100))"""

cursor.execute(sql)

#y='10.0.0.2'

cursor.execute("ALTER TABLE CONTROLLER ADD COLUMN PORT VARCHAR(40)");
cursor.execute("INSERT INTO CONTROLLER(SERVICE,PROVIDER,SWITCH,PORT) VALUES('EL','10.0.1.2','00:00:00:00:00:00:00:01','s4-eth2')")

cursor.execute("INSERT INTO CONTROLLER(SERVICE,PROVIDER,SWITCH,PORT) VALUES('EM','10.0.0.4,10.0.0.5','00:00:00:00:00:00:00:02','s4-eth2')")

cursor.execute("SELECT * FROM CONTROLLER WHERE SERVICE='EB'");
rows=cursor.fetchall()

print cursor.rowcount
for row in rows:
    print row

cursor.execute("SELECT PROVIDER,SWITCH FROM CONTROLLER WHERE SERVICE='EG'");
row=cursor.fetchone()
print row[0];
x=row[0]
print "copied value of row[0]"
print x;
my=x.split(',');
print "length of array after splitting"
print len(my)
print "different value which were separated by comma"
print my[0]
print my[1]

print "SWITCH DPID"
print row[1]


db.commit()


# disconnect from server
db.close()

#! /usr/bin/env python
import socket
import select
import sys
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print 'Socket created'
#s.bind(("localhost",30002))

s.bind(("10.0.0.2",30000))
while 1:
    # receive data from client (data, addr)
    data = s.recv(10240)
    print "check1"
    if not data: 
        break
    f = open("serv_image.jpg",'wb') #open as binary data
    # receives and writes the file
    #l = data.recv(1024)
    st="AISHWARYA"
    print "data.recv()"
    while (data):
	if(data.find(st)>=0):	
		print data.find(st)
		break;
        f.write(data)
        data = s.recv(10240)
f.close()
print "received image"   
    
s.close()

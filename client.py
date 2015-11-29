#!/usr/bin/python
#import pexpect
import os
import time

import socket
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('10.0.0.1' ,33330))

server_address = ('10.0.0.2', 30000)
message = 'This is the message.  It will be repeated.'

def timerInput():
        print "Enter the required timer value between 100 and 999:"
        t_serv1 = raw_input()
        if (int(t_serv1)<100):
                print "Timer value too less. Enter a larger value:"
                t_serv=1
                return t_serv

        elif (int(t_serv1)>999):
                print "Timer value too large. Enter a smaller value:"
                t_serv=1
                return t_serv
        else:
                t_serv = t_serv1
                return t_serv

t_serv=1

while (t_serv==1):
        t_serv = timerInput()

print "Enter the number of services required"

def servinput():
        while 1:

                num_of_services = raw_input()
                if(int(num_of_services)>3):
                        print "Required number of services exceed the maximum limit\nPlease Enter a valid number"
                        continue
                else:
                        return num_of_services

num_of_services = servinput()
print num_of_services
print "Enter the required services\n1.Firewall1: F1\n2.Firewall2: F2\n3.Transcoder: TC"

signal = t_serv + num_of_services

def sendTelnet():
   while (1) :
        ssh_newkey = 'Are you sure you want to continue connecting'
        p=pexpect.spawn('telnet 10.0.0.2')

        i=p.expect([ssh_newkey,'password:',pexpect.EOF, ':','#'])
        if i==3:
                print "Telnet Requesting uname"
                p.sendline('root')
                p.expect([ssh_newkey,'password:',pexpect.EOF, ':','#'])
        if i==0:
                p.sendline('yes')
                i=p.expect([ssh_newkey,'password:',pexpect.EOF])
        if i==1:
                p.sendline("Mahendra")
                p.expect(pexpect.EOF)
        if i==4:
                print "Logged in to the remote host"
                p.sendline('ls')
                p.expect('#')
        elif i==2:
                print "Sorry!.. Connection timedout.. Not able to connect to the remote host"

        pass

        print p.before
        sys.sleep(1)


def serv_input():
        y=1
        while y:
                x = raw_input()
                if (x=="F1" or x=="F2" or x=="TC"):
                        return x
                        y=0
                else:
                        print "Enter a valid service"


for i in range(0,int(num_of_services)):
        x = serv_input()
        signal = signal+x


try:

    # Send data
    message=signal
    count =0
    print >>sys.stderr, 'sending "%s"' % message
    for count in range(3):
        sent = sock.sendto(message, server_address)

    time.sleep(1)
    message ="Hi................."
    for count in range(100):
        sent = sock.sendto(message, server_address)
    # Receive response
    #print >>sys.stderr, 'waiting to receive'
    #data, server = sock.recvfrom(4096)
    #sendTelnet()
    #print >>sys.stderr, 'received "%s"' % data

    time.sleep(5)
finally:
    print >>sys.stderr, 'closing socket'
    sock.close()


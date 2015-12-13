#! /usr/bin/env python
import socket
import select
import sys
import threading
import time
class server_sock(threading.Thread):

	def __init__(self, threadID, name, port):
	        threading.Thread.__init__(self)
        	self.threadID = threadID
        	self.port = port
		self.name = name
	def run(self):	
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		print 'Socket created'
		#s.bind(("localhost",30000))

		s.bind(("10.0.0.3",30000))
		while 1:
			# receive data from client (data, addr)
			data = s.recv(10240)
			print "check1"
			if not data: 
				break
			f = open("vm_image.jpg",'wb') #open as binary data
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

class client_sock(threading.Thread):
	
	def __init__(self, threadID, name, port):
        	threading.Thread.__init__(self)
        	self.threadID = threadID
        	self.port = port
		self.name = name
		
	def run(self):
		s1 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)         # Create a socket object
		host = socket.gethostname() # Get local machine name
		port = 30000               # Reserve a port for your service.
		host1="10.0.0.2"
		s1.bind(('10.0.0.3',33330))
		#s.connect((host1, port))

		f = open('vm_image.jpg','rb')
		print 'Sending...'

		l = f.read(1024)
		while (l):
		#    print 'Sending...'
			print "inside while"
			s1.sendto(l,(host1,port))
			l = f.read(1024)

		buf="AISHWARYA"
		#buf.append("\0")
		print buf

		s1.sendto(buf,("localhost",port))    
		f.close()
		print "Done Sending"
		#s.shutdown(socket.SHUT_WR)
		#print s.recv(1024)
		s1.close()

		
thread_c = client_sock(1, "Thread-client", 30000)
thread_s = server_sock(2, "Thread-server", 33330)

# Start new Threads
thread_s.start()
print "back from server"
#time.sleep(5)
print "*****************sleep!!!!!!!!!!!!!!!!********"
print "execute transcoder"
execfile("./tr.py")
thread_c.start()
#thread_s.pause()
# Add threads to thread list
threads.append(thread_c)
threads.append(thread_s)

# Wait for all threads to complete
for t in threads:
    t.join()
print "Exiting Main Thread"

		

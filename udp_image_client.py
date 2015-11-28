import socket               # Import socket module

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 30000               # Reserve a port for your service.
host1="10.0.0.2"
s.bind(('10.0.0.1',33330))
#s.connect((host1, port))

f = open('aish.jpg','rb')
print 'Sending...'

l = f.read(1024)
while (l):
#    print 'Sending...'
    print "inside while"
    #s.sendto(l,("localhost",port))

    s.sendto(l,(host1,port))
    l = f.read(1024)

buf="AISHWARYA"
#buf.append("\0")
print buf

s.sendto(buf,("localhost",port))    
f.close()
print "Done Sending"
#s.shutdown(socket.SHUT_WR)
#print s.recv(1024)
s.close()


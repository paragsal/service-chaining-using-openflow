import socket
import sys

# Create a TCP/IP socket
HostBSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('127.0.0.1', 33333)
print >>sys.stderr, 'starting up on %s port %s' % server_address
HostBSock.bind(server_address)
HostBSock.listen(5)


while True:
    client, address = HostBSock.accept()
    print >>sys.stderr, '\nwaiting to receive message'
    data = client.recv(4096)
    
    print >>sys.stderr, 'received %s bytes from %s' % (len(data), address)
    print >>sys.stderr, data
    
    if data:
        sent = client.send(data)
        print >>sys.stderr, 'sent %s bytes back to %s' % (sent, address)
 	


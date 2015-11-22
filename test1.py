# Copyright 2012-2013 James McCauley
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
A shortest-path forwarding application.

This is a standalone L2 switch that learns ethernet addresses
across the entire network and picks short paths between them.

You shouldn't really write an application this way -- you should
keep more state in the controller (that is, your flow tables),
and/or you should make your topology more static.  However, this
does (mostly) work. :)

Depends on openflow.discovery
Works with openflow.spanning_tree
"""
import sys
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.recoco import Timer
from collections import defaultdict
from pox.openflow.discovery import Discovery
from pox.lib.util import dpid_to_str
from pox.lib.packet import *
import time
import MySQLdb
import socket, struct
import pox.openflow.discovery

log = core.getLogger()

# Adjacency map.  [sw1][sw2] -> port from sw1 to sw2
adjacency = defaultdict(lambda:defaultdict(lambda:None))

# Switches we know of.  [dpid] -> Switch
switches = {}

# ethaddr -> (switch, port)
mac_map = {}

# [sw1][sw2] -> (distance, intermediate)
path_map = defaultdict(lambda:defaultdict(lambda:(None,None)))

# Waiting path.  (dpid,xid)->WaitingPath
waiting_paths = {}

# Time to not flood in seconds
FLOOD_HOLDDOWN = 5

# Flow timeouts
FLOW_IDLE_TIMEOUT = 1000
FLOW_HARD_TIMEOUT = 3000

# How long is allowable to set up a path?
PATH_SETUP_TIME = 4


def _calc_paths ():
  """
  Essentially Floyd-Warshall algorithm
  """

  def dump ():
    print "check********************"
    print path_map[1][2][0]
    for i in sws:
      for j in sws:
#        print "value of i,j in sws"
#        print i , j
        a = path_map[i][j][0]
#        print path_map[00-00-00-00-00-01][00-00-00-00-00-02][0]
        b = path_map[i][j][1]
        if a is None: a = "*"
#    print "path_map[0] : distance between switches" 
        print a,
      print
        
#    print "mac_map"
#    for key in mac_map:
#      print key
#      print mac_map[key]
  print "check"      
  print path_map[00-00-00-00-00-01][00-00-00-00-00-02][0]
  sws = switches.values()
  path_map.clear()
  print "*******************path_map cleared***********************"
  print "adjacency values"
#  print adjacency[00-00-00-00-00-01][00-00-00-00-00-02][0]
  for key in adjacency:
    print key,adjacency[key]
  print "printing switches dict"
  for key in switches:
    print key,switches[key]
  for k in sws:
    for j,port in adjacency[k].iteritems():
      if port is None: continue
      path_map[k][j] = (1,None)
    path_map[k][k] = (0,None) # distance, intermediate

  #dump()

  for k in sws:
    for i in sws:
      for j in sws:
        if path_map[i][k][0] is not None:
          if path_map[k][j][0] is not None:
            # i -> k -> j exists
            ikj_dist = path_map[i][k][0]+path_map[k][j][0]
            if path_map[i][j][0] is None or ikj_dist < path_map[i][j][0]:
              # i -> k -> j is better than existing
              path_map[i][j] = (ikj_dist, k)

  print "--------------------"
  dump()


def _get_raw_path (src, dst):
  """
  Get a raw path (just a list of nodes to traverse)
  """
  if len(path_map) == 0:
    print "path_map is empty"
    _calc_paths()
  if src is dst:
    # We're here!
    return []
  if path_map[src][dst][0] is None:
    print "path_map[src][dst][0] is None"
    return None
  intermediate = path_map[src][dst][1]
  if intermediate is None:
    # Directly connected
    return []
  return _get_raw_path(src, intermediate) + [intermediate] + \
         _get_raw_path(intermediate, dst)

def _check_path (p):
  """
  Make sure that a path is actually a string of nodes with connected ports

  returns True if path is valid
  """
  for a,b in zip(p[:-1],p[1:]):
    if adjacency[a[0]][b[0]] != a[2]:
      return False
    if adjacency[b[0]][a[0]] != b[1]:
      return False
  return True


def _get_path (src, dst, first_port, final_port):
  """
  Gets a cooked path -- a list of (node,in_port,out_port)
  """
  # Start with a raw path...
#  print "path_map:"
#  for key in path_map:
#    print key,path_map[key]
    
  if src == dst:
    path = [src]
  else:
    path = _get_raw_path(src, dst)
    print "before return in get_path***************"
    print "length of path_map is "
    print len(path_map)
    for key in path_map:
      print key,path_map[key]
    print path_map[src][dst][0]
    print path_map[src][dst][1]
    print path_map[00-00-00-00-00-01][00-00-00-00-00-03][0]
    print path
    print src
    print dst
    if path is None: return None
    path = [src] + path + [dst]
  print"path from src to dst in _get_path"
  print path 
  # Now add the ports
  r = []
  in_port = first_port
  for s1,s2 in zip(path[:-1],path[1:]):
    out_port = adjacency[s1][s2]
    r.append((s1,in_port,out_port))
    in_port = adjacency[s2][s1]
  r.append((dst,in_port,final_port))

  assert _check_path(r), "Illegal path!"

  return r

#**********function added by Sumit ***************   
def fetch_service_info(serv_arr):
  length=len(serv_arr)
  i=0
  print "@@@@@@@@@@@@@@@@@@@@@@@@@@@serv array is " 
  print serv_arr
  for key in switches:
    print switches[key]
    print key
  if len(path_map) == 0: _calc_paths()
  service_switch=[]
  service_port=[]   #port to which VM is connected with service switch
  db = MySQLdb.connect("localhost","root","root","test1" )
    # prepare a cursor object using cursor() method
  cursor = db.cursor()
  while i<length:
    cursor.execute("SELECT SWITCH FROM CONTROLLER1 WHERE SERVICE=%s",(serv_arr[i]))
    row=cursor.fetchone()
#    switch_list=row[0] 
    switch_list=row[0].split(',')
    len_row=len(switch_list)
    print "len row"
    print len_row
    print "switches are:"
    print row
    print row[0]
#assuming all VMs are connected to service swithces through same ports
    cursor.execute("SELECT PORT FROM CONTROLLER1 WHERE SERVICE=%s",(serv_arr[i]))
    row_port=cursor.fetchone()
    service_port.append(int(row_port[0]))
    j=0
    k=0
    if len_row == 1:
      service_switch.append(int(row[0]))
#      service_port.append(int(row_port[0])    #it has to be included as different switches may be connected to VMs via different ports
    elif len_row > 1:                 #if more than one service switch available, then find nearest switch and append it to service_switch
      if i==0:
#        sw1=self
        sw1=1
      else:
        sw1=int(service_switch[i-1])
        mini=1111110  #some random large value            
#????? assuming that path_map has already been generated, need to check if path_map[][DPID]takes DPID or mac addresses as keys
      while j<len_row:                          
        if mini>path_map[switches[sw1]][switches[int(switch_list[j])]][0]: #finding the switch closest to last service switch
          mini=path_map[switches[sw1]][switches[int(switch_list[j])]][0]    
          k=j
        print "distance between sw1 and switch_lst[j]"
        print path_map[switches[sw1]][switches[int(switch_list[j])]][0]  
        j=j+1
      print "minimum distance switch and value of j "
      print k,j,mini   
      service_switch.append(int(switch_list[k]))
#     service_port.append(int(switch_list[k]))
      print service_switch                    
      print service_port      
    i=i+1
  db.close() 
  print 'printing service switch'
  print service_switch
  print 'service port'
  print service_port 
  return service_switch, service_port
          
#**********changes by Sumit till here *************************   
  

class WaitingPath (object):
  """
  A path which is waiting for its path to be established
  """
  def __init__ (self, path, packet):
    """
    xids is a sequence of (dpid,xid)
    first_switch is the DPID where the packet came from
    packet is something that can be sent in a packet_out
    """
    self.expires_at = time.time() + PATH_SETUP_TIME
    self.path = path
    self.first_switch = path[0][0].dpid
    self.xids = set()
    self.packet = packet

    if len(waiting_paths) > 1000:
      WaitingPath.expire_waiting_paths()

  def add_xid (self, dpid, xid):
    self.xids.add((dpid,xid))
    waiting_paths[(dpid,xid)] = self

  @property
  def is_expired (self):
    return time.time() >= self.expires_at

  def notify (self, event):
    """
    Called when a barrier has been received
    """
    self.xids.discard((event.dpid,event.xid))
    if len(self.xids) == 0:
      # Done!
      if self.packet:
        log.debug("Sending delayed packet out %s"
                  % (dpid_to_str(self.first_switch),))
        msg = of.ofp_packet_out(data=self.packet,
            action=of.ofp_action_output(port=of.OFPP_TABLE))
        core.openflow.sendToDPID(self.first_switch, msg)

      core.l2_multi.raiseEvent(PathInstalled(self.path))


  @staticmethod
  def expire_waiting_paths ():
    packets = set(waiting_paths.values())
    killed = 0
    for p in packets:
      if p.is_expired:
        killed += 1
        for entry in p.xids:
          waiting_paths.pop(entry, None)
    if killed:
      log.error("%i paths failed to install" % (killed,))


class PathInstalled (Event):
  """
  Fired when a path is installed
  """
  def __init__ (self, path):
    Event.__init__(self)
    self.path = path


class Switch (EventMixin):
  def __init__ (self):
    self.connection = None
    self.ports = None
    self.dpid = None
    self._listeners = None
    self._connected_at = None

  def __repr__ (self):
    return dpid_to_str(self.dpid)

  def _install (self, switch, in_port, out_port, match, buf = None):
    print "inside _install"
    print "IN PORT ********** ",in_port
    msg = of.ofp_flow_mod()
    msg.match = match
    msg.match.in_port = in_port
    msg.idle_timeout = FLOW_IDLE_TIMEOUT
    msg.hard_timeout = FLOW_HARD_TIMEOUT
    msg.actions.append(of.ofp_action_output(port = out_port))
    msg.buffer_id = buf
    switch.connection.send(msg)
    print "******message sent to switch:"
    print switch

  def _install_path (self, p, match, packet_in=None):
    print "inside _install_path"
    wp = WaitingPath(p, packet_in)
    for sw,in_port,out_port in p:
      self._install(sw, in_port, out_port, match)
      msg = of.ofp_barrier_request()
      sw.connection.send(msg)
      wp.add_xid(sw.dpid,msg.xid)

#************** Added by Sumit : to intall flows on intermediate and last switch switches *************#
  def _install_path_new (self, p, match):
#    wp = WaitingPath(p, packet_in)
    print "inside _install_path_new"
    for sw,in_port,out_port in p:
      self._install(sw, in_port, out_port, match)
      self._install(sw, out_port,in_port,match.flip()) #installing path in reverse direction from host B to host A
#      msg = of.ofp_barrier_request()
#      sw.connection.send(msg)
#      wp.add_xid(sw.dpid,msg.xid)

#***********************added till here ************************************************          
  def install_path (self, dst_sw, last_port, match, event):
    """
    Attempts to install a path between this switch and some destination
    """
    print "inside install_path and switches in sequence are self,dst_sw,event.port,last_port"
    print str(self)+" "+str(dst_sw)+" "+str(event.port)+" "+str(last_port)
    print "printing mac_map again"
    for key in mac_map:
      print key
      print mac_map[key]
    p = _get_path(self, dst_sw, event.port, last_port)
    print p
    if p is None:
      log.warning("Can't get from %s to %s", match.dl_src, match.dl_dst)
sumit
      import pox.lib.packet as pkt

      if (match.dl_type == pkt.ethernet.IP_TYPE and
          event.parsed.find('ipv4')):
        # It's IP -- let's send a destination unreachable
        log.debug("Dest unreachable (%s -> %s)",
                  match.dl_src, match.dl_dst)

        from pox.lib.addresses import EthAddr
        e = pkt.ethernet()
        e.src = EthAddr(dpid_to_str(self.dpid)) #FIXME: Hmm...
        e.dst = match.dl_src
        e.type = e.IP_TYPE
        ipp = pkt.ipv4()
        ipp.protocol = ipp.ICMP_PROTOCOL
        ipp.srcip = match.nw_dst #FIXME: Ridiculous
        ipp.dstip = match.nw_src
        icmp = pkt.icmp()
        icmp.type = pkt.ICMP.TYPE_DEST_UNREACH
        icmp.code = pkt.ICMP.CODE_UNREACH_HOST
        orig_ip = event.parsed.find('ipv4')

        d = orig_ip.pack()
        d = d[:orig_ip.hl * 4 + 8]
        import struct
        d = struct.pack("!HH", 0,0) + d #FIXME: MTU
        icmp.payload = d
        ipp.payload = icmp
        e.payload = ipp
        msg = of.ofp_packet_out()
        msg.actions.append(of.ofp_action_output(port = event.port))
        msg.data = e.pack()
        self.connection.send(msg)

      return

    log.debug("Installing path for %s -> %s %04x (%i hops)",
        match.dl_src, match.dl_dst, match.dl_type, len(p))

    # We have a path -- install it
    self._install_path(p, match, event.ofp)

    # Now reverse it and install it backwards
    # (we'll just assume that will work)
#Sumit : We  need a reverse path for getting the packets like acks, etc from host B to host A
    p = [(sw,out_port,in_port) for sw,in_port,out_port in p]
    self._install_path(p, match.flip())
 
#*********************Added by Sumit to get intermediate switched between service switch ***************
# ???????????????? indentation needs to be checked before testing ???????????????
  def install_path_new(self,src_sw, dst_sw, first_port, last_port, match):
    print "inside install_path_new*******************",first_port
    p = _get_path(src_sw, dst_sw, first_port, last_port)
    if p is None:
      log.warning("Can't get from %s to %s", match.dl_src, match.dl_dst)
    else:
      log.debug("Installing path for %s -> %s %04x (%i hops)",
      match.dl_src, match.dl_dst, match.dl_type, len(p))
      # We have a path -- install it
      self._install_path_new(p, match)

#********************Changes till here *******************************************
          
  def _handle_PacketIn (self, event):
    def flood ():
      """ Floods the packet """
      #if self.is_holding_down:
      #  log.warning("Not flooding -- holddown active")
      log.warning("Flooding the packet")
      msg = of.ofp_packet_out()
      # OFPP_FLOOD is optional; some switches may need OFPP_ALL
      msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
      msg.buffer_id = event.ofp.buffer_id
      msg.in_port = event.port
      self.connection.send(msg)
    
    def drop ():
      # Kill the buffer
      if event.ofp.buffer_id is not None:
        msg = of.ofp_packet_out()
        msg.buffer_id = event.ofp.buffer_id
        event.ofp.buffer_id = None # Mark is dead
        msg.in_port = event.port
        self.connection.send(msg)

    packet = event.parsed
#*************changes made by mahendra ****************/
    self.service_name_array = [];
    ethr_hdr_len = packet.hdr_len
    
    print "Ethernet Payload length ->",packet.payload_len
    if packet.type != ethernet.ARP_TYPE:
        #if packet.type == ethernet.IP_TYPE and packet.payload_len >= 60:
        #Skip Minimum length packet which doesn't contain any data

    	ip_hdr_len = packet.next.hl *4

	if packet.next.protocol !=ipv4.ICMP_PROTOCOL:
		#Check if it is TCP SYN, SYN+ACK, or ACK packets
		if (packet.next.protocol == ipv4.TCP_PROTOCOL) :
			if packet.next.next.SYN or packet.next.next.ACK or packet.next.next.FIN or packet.next.next.RST :
				print ">>>>TCP Connection establishment message Observed <<<<<"	
				if (packet.next.next.payload_len == 0) :
					print "%%%% No Payload %%%"
					flood()
					return

    		transport_hdr_len = packet.next.next.hdr_len
    		tot_hl = ethr_hdr_len + ip_hdr_len + transport_hdr_len
    		print "Total header length ->", tot_hl
    		print "Ethernet Payload length ->",packet.payload_len
        	print packet.next.dstip
        
        	print "*"*20
        	print packet.next.next.raw[8:]
        	print "*"*20
        	data = packet.next.next.raw[8:]
        	self.timer = data[:1] #Sumit: changed the value from data[:2] to data[:1] as timer is only 1 byte
        	print "Timer -", self.timer
        	self.tot_srvc = data[1:2] #Sumit: service length is only 1 byte
        	print " Total Service -",self.tot_srvc
        	data = data[2:] #Sumit:

        	j=0;

        	for i in range(0,int(self.tot_srvc)) :
           		self.service_name_array.append(data[j:j+2] ); 
           		j+=2
           		print self.service_name_array[i]

        	data = data[:j] 

#*****************changes made by mahendra ends here *****************

    loc = (self, event.port) # Place we saw this ethaddr
    oldloc = mac_map.get(packet.src) # Place we last saw this ethaddr

    if packet.effective_ethertype == packet.LLDP_TYPE:
      drop()
      return

    if oldloc is None:
      if packet.src.is_multicast == False:
        mac_map[packet.src] = loc # Learn position for ethaddr
        log.debug("Learned %s at %s.%i", packet.src, loc[0], loc[1])
    elif oldloc != loc:
      # ethaddr seen at different place!
      if core.openflow_discovery.is_edge_port(loc[0].dpid, loc[1]):
        # New place is another "plain" port (probably)
        log.debug("%s moved from %s.%i to %s.%i?", packet.src,
                  dpid_to_str(oldloc[0].dpid), oldloc[1],
                  dpid_to_str(   loc[0].dpid),    loc[1])
        if packet.src.is_multicast == False:
          mac_map[packet.src] = loc # Learn position for ethaddr
          log.debug("Learned %s at %s.%i", packet.src, loc[0], loc[1])
      elif packet.dst.is_multicast == False:
        # New place is a switch-to-switch port!
        # Hopefully, this is a packet we're flooding because we didn't
        # know the destination, and not because it's somehow not on a
        # path that we expect it to be on.
        # If spanning_tree is running, we might check that this port is
        # on the spanning tree (it should be).
        if packet.dst in mac_map:
          # Unfortunately, we know the destination.  It's possible that
          # we learned it while it was in flight, but it's also possible
          # that something has gone wrong.
          log.warning("Packet from %s to known destination %s arrived "
                      "at %s.%i without flow", packet.src, packet.dst,
                      dpid_to_str(self.dpid), event.port)


    if packet.dst.is_multicast:
      log.debug("Flood multicast from %s", packet.src)
      print "&&"*20
      flood()
    else:
      if packet.dst not in mac_map:
        log.debug("%s unknown -- flooding" % (packet.dst,))
        print "******************************************************"
        flood()
      else:
#*****************changes made by Sumit **********************
        serv_switch=[]
        serving_port=[]
        if len(self.service_name_array) ==0:
                flood()
                return;

        serv_switch, serving_port=fetch_service_info(self.service_name_array)
        
        print "serv_switch and serv_port"
        print serv_switch
        print serv_switch[0]
#        print dpid_to_str(serv_switch[0])

#        print switches[00-00-00-00-00-01]          
        print serving_port          
        dest = mac_map[packet.dst]
        len_serv_switch=len(serv_switch)
#               serv_switch.append(dest[0])
#               last_port=dest[1]
#               port_serv_switch=adjacency[serv_switch[0]][self]                #port at serv_switch[0] to connect to this switch
#               len_serv_switch=len(serv_switch)
        match = of.ofp_match.from_packet(packet)
        self.install_path(switches[serv_switch[0]],serving_port[0], match, event) #in case only one serv_switch, install path to it and then to dest
        i=0
        if len_serv_switch>1: #install flow on all service switches and destination in case of more than 1 service switch
          while i<len_serv_switch-1:
            self.install_path_new(switches[serv_switch[i]],switches[serv_switch[i+1]],serving_port[i],serving_port[i+1],match)
            i=i+1
          self.install_path_new(serv_switch[i],dest[0],serving_port[i-1],dest[1], match)
        self.install_path_new(serv_switch[0],dest[0],serving_port[0],dest[1],match)  
#******************Changes till here *****************************

  def disconnect (self):
    if self.connection is not None:
      log.debug("Disconnect %s" % (self.connection,))
      self.connection.removeListeners(self._listeners)
      self.connection = None
      self._listeners = None

  def connect (self, connection):
    if self.dpid is None:
      self.dpid = connection.dpid
    assert self.dpid == connection.dpid
    if self.ports is None:
      self.ports = connection.features.ports
    self.disconnect()
    log.debug("Connect %s" % (connection,))
    self.connection = connection
    self._listeners = self.listenTo(connection)
    self._connected_at = time.time()

  @property
  def is_holding_down (self):
    if self._connected_at is None: 
        print "###"*20
        return True
    if time.time() - self._connected_at > FLOOD_HOLDDOWN:
      return False
    return True

  def _handle_ConnectionDown (self, event):
    self.disconnect()


class l2_multi (EventMixin):

  _eventMixin_events = set([
    PathInstalled,
  ])

  def __init__ (self):
    # Listen to dependencies
    def startup ():
      core.openflow.addListeners(self, priority=0)
      core.openflow_discovery.addListeners(self)
    core.call_when_ready(startup, ('openflow','openflow_discovery'))

  def _handle_LinkEvent (self, event):
    def flip (link):
      return Discovery.Link(link[2],link[3], link[0],link[1])

    l = event.link
    sw1 = switches[l.dpid1]
    sw2 = switches[l.dpid2]
    print "l.dpid1 and dpid2"
    print l.dpid1 , l.dpid2
    print sw1, sw2
    # Invalidate all flows and path info.
    # For link adds, this makes sure that if a new link leads to an
    # improved path, we use it.
    # For link removals, this makes sure that we don't use a
    # path that may have been broken.
    #NOTE: This could be radically improved! (e.g., not *ALL* paths break)
    clear = of.ofp_flow_mod(command=of.OFPFC_DELETE)
    for sw in switches.itervalues():
      if sw.connection is None: continue
      sw.connection.send(clear)
    path_map.clear()

    if event.removed:
      # This link no longer okay
      if sw2 in adjacency[sw1]: del adjacency[sw1][sw2]
      if sw1 in adjacency[sw2]: del adjacency[sw2][sw1]

      # But maybe there's another way to connect these...
      for ll in core.openflow_discovery.adjacency:
        if ll.dpid1 == l.dpid1 and ll.dpid2 == l.dpid2:
          if flip(ll) in core.openflow_discovery.adjacency:
            # Yup, link goes both ways
            adjacency[sw1][sw2] = ll.port1
            adjacency[sw2][sw1] = ll.port2
            # Fixed -- new link chosen to connect these
            break
    else:
      # If we already consider these nodes connected, we can
      # ignore this link up.
      # Otherwise, we might be interested...
      if adjacency[sw1][sw2] is None:
        # These previously weren't connected.  If the link
        # exists in both directions, we consider them connected now.
        if flip(l) in core.openflow_discovery.adjacency:
          # Yup, link goes both ways -- connected!
          adjacency[sw1][sw2] = l.port1
          adjacency[sw2][sw1] = l.port2

      # If we have learned a MAC on this port which we now know to
      # be connected to a switch, unlearn it.
      bad_macs = set()
      for mac,(sw,port) in mac_map.iteritems():
        if sw is sw1 and port == l.port1: bad_macs.add(mac)
        if sw is sw2 and port == l.port2: bad_macs.add(mac)
      for mac in bad_macs:
        log.debug("Unlearned %s", mac)
        del mac_map[mac]

  def _handle_ConnectionUp (self, event):
    sw = switches.get(event.dpid)
    if sw is None:
      # New switch
      sw = Switch()
      switches[event.dpid] = sw
      sw.connect(event.connection)
    else:
      sw.connect(event.connection)

  def _handle_BarrierIn (self, event):
    wp = waiting_paths.pop((event.dpid,event.xid), None)
    if not wp:
      #log.info("No waiting packet %s,%s", event.dpid, event.xid)
      return
    #log.debug("Notify waiting packet %s,%s", event.dpid, event.xid)
    wp.notify(event)


def launch ():
  core.registerNew(l2_multi)

  timeout = min(max(PATH_SETUP_TIME, 5) * 2, 15)
  Timer(timeout, WaitingPath.expire_waiting_paths, recurring=True)
  #pox.openflow.discovery.launch();
  import pox.openflow.spanning_tree
  pox.openflow.spanning_tree.launch()



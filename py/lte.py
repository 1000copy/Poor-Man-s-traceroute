#!/usr/bin/env python  
import os, sys, socket, struct, select, time  

ICMP_ECHO_REQUEST = 8 
ICMP_ECHO_REPLY  = 0; 
ICMP_TIMEOUT   = 11; 
 
    
import unittest

class Trace:
    def __init__(self):
        pass
    def checksum(self,source_string): 
        sum = 0 
        countTo = (len(source_string)/2)*2 
        count = 0 
        while count<countTo: 
            thisVal = ord(source_string[count + 1])*256 + ord(source_string[count]) 
            sum = sum + thisVal 
            sum = sum & 0xffffffff # Necessary? 
            count = count + 2 
     
        if countTo<len(source_string): 
            sum = sum + ord(source_string[len(source_string) - 1]) 
            sum = sum & 0xffffffff # Necessary? 
     
        sum = (sum >> 16)  +  (sum & 0xffff) 
        sum = sum + (sum >> 16) 
        answer = ~sum 
        answer = answer & 0xffff 
     
        # Swap bytes. Bugger me if I know why. 
        answer = answer >> 8 | (answer << 8 & 0xff00) 
     
        return answer 
     
# typedef struct
# {
#  unsigned char hdr_len :4;  // length of the header
#  unsigned char version :4;  // version of IP
#  unsigned char tos;   // type of service
#  unsigned short total_len;  // total length of the packet
#  unsigned short identifier;  // unique identifier
#  unsigned short frag_and_flags; // flags
#  unsigned char ttl;   // time to live
#  unsigned char protocol;  // protocol (TCP, UDP etc)
#  unsigned short checksum;  // IP checksum
#  unsigned long sourceIP;  // source IP address
#  unsigned long destIP;   // destination IP address
# } IP_HEADER;

    def echo_reply_decode(self, ID, timeout):         
        # (reply,ttl exceed,timeout),ip address ,delay
        timeLeft = timeout 
        while True: 
            startedSelect = time.clock() 
            whatReady = select.select([self.my_socket], [], [], timeLeft) 
            howLongInSelect = (time.clock() - startedSelect) 
            if whatReady[0] == []: # Timeout 
                return      
            timeReceived = time.clock() 
            recPacket, addr = self.my_socket.recvfrom(1024) 
            icmpHeader = recPacket[20:28] 
            type, code, checksum, packetID, sequence = \
                struct.unpack( 
                    "bbHHh", icmpHeader 
                )      
            # print(type)        
            # ip = recPacket[16:20] # destination addr
            ip = recPacket[12:16] # src addr
            if type ==  ICMP_ECHO_REPLY:        
                if packetID == ID: 
                    bytesInDouble = struct.calcsize("d") 
                    timeSent = struct.unpack("d", recPacket[28:28 + bytesInDouble])[0]                     
                    return 1,int2ip(ip),timeReceived - timeSent
            if type ==  ICMP_TIMEOUT:                       
                    # print("Timeout")
                    def int2ip(addr):                                                               
                        # return socket.inet_ntoa(struct.pack("!I", addr))                    
                        return socket.inet_ntoa(addr)
                    print 1,(int2ip(ip)),0
                    return 

            timeLeft = timeLeft - howLongInSelect 
            if timeLeft <= 0: 
                return None,0,0
    def echo_request(self, dest_addr, ID): 
        dest_addr  =  socket.gethostbyname(dest_addr)      
        # Header is type (8), code (8), checksum (16), id (16), sequence (16) 
        my_checksum = 0      
        # Make a dummy heder with a 0 checksum. 
        header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, my_checksum, ID, 1) 
        bytesInDouble = struct.calcsize("d") 
        data = (192 - bytesInDouble) * "Q" 
        data = struct.pack("d", time.clock()) + data      
        # Calculate the checksum on the data and the dummy header. 
        my_checksum = self.checksum(header + data)      
        # Now that we have the right checksum, we put that in. It's just easier 
        # to make up a new header than to stuff it into the dummy. 
        header = struct.pack( "bbHHh", 
            ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), ID, 1 ) 
        packet = header + data 
        self.my_socket.sendto(packet, (dest_addr, 1)) # Don't know about the 1      
    def set_ttl(self,ttl):
        self.my_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
    def socket_ready(self):
        icmp = socket.getprotobyname("icmp") 
        try: 
            self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)                     
        except socket.error, (errno, msg): 
            if errno == 1:                 
                raise socket.error(msg+"- tip: running as root." ) 
            else:
                raise # raise the original error 
    def do_one(self,dest_addr, timeout,ttl): 
        """
        Returns either the delay (in seconds) or none on timeout.
        """ 
        self.socket_ready()
        self.set_ttl(ttl)
        my_ID = os.getpid() & 0xFFFF      
        self.echo_request(dest_addr, my_ID) 
        flag,addr,delay = self.echo_reply_decode( my_ID, timeout)              
        if flag  ==  None: 
            print "\ttimeout"                      
        else: 
            delay  =  delay * 1000 
            print "\t%s in %0.4fms" % addr,delay  
            return 
        self.my_socket.close()
     
    def do(self,dest_addr, timeout = 3, max_hops = 30): 
        print "ping %s...\n" % dest_addr, 
        for i in xrange(max_hops):         
            try: 
                print ("%s." % i)
                self.do_one(dest_addr, timeout,i)                
            except socket.gaierror, e: 
                print "failed. (socket error: '%s')" % e[1] 
                break  
class tt(unittest.TestCase):
    def setUp(self):
        self.t= Trace()
    def test_sample(self):
        self.t.do("163.com") 
if __name__ == '__main__':
    unittest.main()
# if __name__ == '__main__': 
#     ping("163.com") 
"""

    Echo or Echo Reply Message

    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |     Type      |     Code      |          Checksum             |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |           Identifier          |        Sequence Number        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |     Data ...
   +-+-+-+-+-

      The identifier and sequence number may be used by the echo sender
      to aid in matching the replies with the echo requests.  For
      example, the identifier might be used like a port in TCP or UDP to
      identify a session, and the sequence number might be incremented
      on each echo request sent.  The echoer returns these same values
      in the echo reply.  
""" 
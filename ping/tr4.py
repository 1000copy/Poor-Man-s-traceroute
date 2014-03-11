#! /usr/bin/env python
 
"""
Sample usage:
 
sudo python traceroute.py www.google.com
[sudo] password for gene:
WARNING: No route found for IPv6 destination :: (no default route?)
1 -> 10.0.0.138
2 -> 172.18.212.13
3 -> 172.18.69.149
4 -> 172.18.241.101
5 -> 203.45.53.237
6 -> 203.50.44.13
7 -> 203.50.11.72
8 -> 203.50.11.95
9 -> 139.130.213.54
10 -> 66.249.95.234
11 -> 72.14.236.181
12 -> 74.125.237.209
 
"""
 
 
import sys
import os
from scapy.all import sr1,IP,ICMP
 
if len(sys.argv) != 2:
    sys.exit('Usage: traceroute.py <remote host>')
 
# we start with 1
ttl = 1
while 1:
    p=sr1(IP(dst=sys.argv[1],ttl=ttl)/ICMP(id=os.getpid()),
          verbose=0)
    # if time exceeded due to TTL exceeded
    if p[ICMP].type == 11 and p[ICMP].code == 0:
        print ttl, '->', p.src
        ttl += 1
    elif p[ICMP].type == 0:
        print ttl, '->', p.src
        break
 
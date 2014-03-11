#!/usr/bin/python

import sys
import os 
import re 
import urllib
import subprocess

def getlocation(ip):
    result = urllib.urlopen("http://www.ip138.com/ips.asp?ip=%s&action=2" % ip)
    res = result.readlines()
    print res

    result.close()
    for i in res:
        if re.match(".*ul class=\"ul1\".*",i):
            ipblock=i
    if 'ipblock' in dir():
        add1 = ipblock.split("<")[3].split(">")[1].decode('gb2312')[6:].encode('utf8')
        add2 = ipblock.split("<")[5].split(">")[1].decode('gb2312')[6:].encode('utf8')
        if add1 == add2:
            return "\t\t\t"+add1
        else:
            return "\t\t\t"+add1+"\tOR\t"+add2

if len(sys.argv) < 2: 
    print "Usage: %s {hostname|ip}" % sys.argv[0]
    sys.exit()
else:
    host = sys.argv[1]
line = "3     5 ms     2 ms     2 ms  182.151.192.109"
print line
ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', line )
print ip
print getlocation("202.98.98.5")
exit()

try:
    p = subprocess.Popen(['tracert',host],stdout=subprocess.PIPE)
    while True:
        line = p.stdout.readline()
        if not line:
            break        
        ip  = re.findall( r'[0-9]+(?:\.[0-9]+){3}', line )
        if ip and len(ip)>0:
            try:
                print ip[0]
                l =  getlocation(ip[0]) 
                if l:
                    print line+ l
                else:
                    print line +":none"
            except IndexError,e: 
                print e,
        else:
            print line,
except (KeyboardInterrupt,SystemExit):
    sys.exit()



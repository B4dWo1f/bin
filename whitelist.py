#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from base64 import b64encode as encode
from base64 import b64decode as decode
import ipaddress as IP
import os
here = os.path.dirname(os.path.realpath(__file__))
HOME = os.environ['HOME']
HOSTNAME = os.uname()[1]



## General parameters
whitelist_local = '%s/.whitelist'%(HOME)
whitelist_server = '%s/.whitelist.kasterborous'%(HOME)


## Dummy parameters
tmp_whitelist = '/tmp/whitelist'


## Current local IPs
my_IPs = os.popen('hostname -I').read().split()
# complete list of trustable IP's [local, loopback, whitelist from server...]
whitelist = [IP.ip_address(ip) for ip in my_IPs]


## loopback IPs (from /etc/hosts)
hosts = '/etc/hosts'
aux = open(hosts,'r').read().splitlines()
for l in aux:
   try: whitelist.append( IP.ip_address(l.split()[0]) )
   #   if l.split()[0].split('.')[0] == '127':
   #      whitelist.append( IP.ip_address(l.split()[0]) )
   except: pass
print(whitelist)
exit()

## Server whitelist
usr,dom = open('%s/server.private'%(here),'r').read().splitlines()
usr = str(decode(usr),'utf-8')
dom = str(decode(dom),'utf-8')
com = 'scp -q %s@%s:.whitelist %s'%(usr,dom,tmp_whitelist)
os.system(com)
com = 'mv %s %s'%(tmp_whitelist, whitelist_server)
os.system(com)


## Get trustable ips from personal Server
try:
   with open(whitelist_server,'r') as f: aux = f.readlines()
   f.close()
   for l in aux:
      whitelist.append( IP.ip_address(l.lstrip().rstrip()) )
except: pass  # If server is down or other error


## Simplify and sort the list of whitelisted IPs
whitelist = list(sorted(set(whitelist)))
whitelist = [ip.exploded for ip in whitelist]


## Save file
f = open(whitelist_local, 'w')
f.write( '\n'.join(whitelist) + '\n')
f.close()

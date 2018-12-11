#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import ipaddress as IP
from tools import get_public_IP,files
HOME = os.getenv('HOME')


Wlist = []
## Retrieve current public IP
Wlist.append( IP.ip_address(get_public_IP()) )

## Retrieve current local IP
my_IPs = os.popen('hostname -I').read().split()
Wlist += [IP.ip_address(ip) for ip in my_IPs]

## loopback IPs (from /etc/hosts)
hosts = '/etc/hosts'
aux = open(hosts,'r').read().splitlines()
for l in aux:
   try: Wlist.append( IP.ip_address(l.split()[0]) )
   except: pass


## Read reported IPs from friendly clients
for f in files('/share/',abspath=True):
   ip = open(f,'r').read().strip()
   Wlist.append(ip)

Wlist = set(Wlist)

## Write the whitelist
with open(HOME+'/.whitelist','w') as f:
   for ip in Wlist:
      f.write(str(ip)+'\n')
f.close()

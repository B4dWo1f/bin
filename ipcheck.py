#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from mytools import get_public_IP
import os
HOME = os.environ['HOME']


IPfile = HOME+'/.IP'
IP = get_public_IP()

## Check if the IP has changed
try:
   with open(IPfile,'r') as f:
      previous = f.readlines()[0].lstrip().rstrip()
except: previous = '*.*.*.*'  # No previous IP

## If it has changed, report it
if previous != IP:
   if IP != None:
      with open(IPfile,'w') as f:
         f.write(str(IP)+'\n')
      f.close()

#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
 The purpose of this script is to report current ip from friendly devices
"""

from base64 import b64decode as decode
from base64 import b64encode as encode
from mytools import get_public_IP
import os
here = os.path.dirname(os.path.realpath(__file__))
HOME = os.getenv('HOME')
HOSTNAME = os.uname()[1]


f_ip = HOME + '/.IP'

## Get server information
usr,port,dom = open('%s/server.private'%(here),'r').read().splitlines()
usr = str(decode(usr),'utf-8')
port = int(str(decode(port),'utf-8'))
dom = str(decode(dom),'utf-8')


try: previous_IP = open(f_ip,'r').read().strip()
except FileNotFoundError: previous_IP = ''

## Get current public IP
current_IP = get_public_IP()
# send to server if information changed
if str(current_IP) != previous_IP:
   with open(f_ip,'w') as f:
      f.write(str(current_IP)+'\n')
   f.close()
   send = 'scp -q -P%s %s %s@%s:/share/%s.ip'%(port, f_ip, usr,dom, HOSTNAME)
   os.system(send)
else: pass

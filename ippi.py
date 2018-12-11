#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
 The purpose of this script is to report current ip from friendly devices
"""

from base64 import b64decode as decode
from base64 import b64encode as encode
from tools import get_public_IP
import os
here = os.path.dirname(os.path.realpath(__file__))
HOME = os.getenv('HOME')
HOSTNAME = os.uname()[1]


f_ip = HOME + '/.IP'

usr,dom = open('%s/server.private'%(here),'r').read().splitlines()
usr = str(decode(usr),'utf-8')
dom = str(decode(dom),'utf-8')


previous_IP = open(f_ip,'r').read().strip()

current_IP = get_public_IP()
if str(current_IP) != previous_IP:
   with open(f_ip,'w') as f:
      f.write(str(current_IP)+'\n')
   f.close()
   send = 'scp %s %s@%s:%s.ip'%(f_ip, usr,dom, HOSTNAME)
   print(send)
else: pass

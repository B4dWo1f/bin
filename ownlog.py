#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from time import sleep
from random import uniform
import os

# wait random time
sleep(uniform(5,15))


usr = 'noel'
srv = 'kasterborous.ddns.net'
r_file = 'mylogs/owncloud.log'  #remote file
l_file = '/tmp/owncloud.log'  #local file
f_file = '~/.owncloud.log'  #final file


bring = 'scp -q %s@%s:%s %s'%(usr,srv,r_file,l_file)
move = 'mv %s %s'%(l_file,f_file)


resp = os.popen('gnome-screensaver-command -q | grep "is active"').read()
if len(resp) == 0:  # computer is not sleeping
   from tools import internet
   if internet():   # there is internet connection
      os.system(bring)
      os.system(move)
#   else: print('No internet')
#else: print('Computer sleeping')

#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
This script should be added to crontab to check some parameters so the conkyrc
is automatically updated when needed
"""

import os
HOME = os.getenv('HOME')
DISPLAY = os.getenv('DISPLAY')


command = 'DISPLAY=%s '%(DISPLAY) + HOME + '/configs/conky/setup_conky.py'
conkyrc = HOME+'/.conkyrc'

## If new network interface appears
# current interfaces analyzed by conky
current = os.popen('grep addr %s'%(conkyrc)).read().splitlines()
nets = [x.split('addr')[1].split('}')[0].lstrip().rstrip() for x in current]
nets = sorted(nets)
# actual network interfaces
networks = os.popen('/sbin/ifconfig -s | cut -d " " -f 1').read().splitlines()
try: networks.remove('Iface')
except: pass
try: networks.remove('lo')
except: pass
networks = sorted(networks)
if networks != nets:
   #print('***** Need to update conkyrc')
   os.system('DISPLAY=%s notify-send "Updating conkyrc"'%(DISPLAY))
   os.system(command)

## If owncloud log appears
# currently checking owncloud.log?
current = os.popen('grep owncloud.log %s'%(conkyrc)).read()
if not len(current) and os.path.isfile(HOME+'/.owncloud.log'):
   #print('***** Need to update conkyrc')
   os.system('DISPLAY=%s notify-send "Updating conkyrc"'%(DISPLAY))
   os.system(command)

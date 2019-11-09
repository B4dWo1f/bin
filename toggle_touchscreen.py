#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os

com = 'xinput --list | grep Touchscreen'
id_touchscreen = int(os.popen(com).read().split()[-4].split('=')[-1])

com = 'xinput list-props %s | grep "Device Enabled"'%(id_touchscreen)
enabled = bool( int(os.popen(com).read().split()[-1]) )

if enabled:
   com = 'xinput disable %s'%(id_touchscreen)
   os.system(com)
   com = 'notify-send "TouchScreen Disabled"'
   os.system(com)
else:
   com = 'xinput enable %s'%(id_touchscreen)
   os.system(com)
   com = 'notify-send "TouchScreen Enabled"'
   os.system(com)

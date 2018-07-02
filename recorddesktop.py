#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
this script should start/stop recording the desktop
"""

import os

resp = os.popen('ps -e | grep recordmydesktop').read()
if len(resp) == 0: is_running = False
else: is_running = True


if is_running:
   #print('Stopping "recordmydesktop"')
   os.system('killall recordmydesktop')
else:
   #print('Starting "recordmydesktop"')
   os.system('recordmydesktop --on-the-fly-encoding')

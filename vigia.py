#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
 TO-DO:
 - rename!!
"""

import os
import sys
from time import sleep
from mailator import send_mail

program = sys.argv[1]

com = 'ps -e | grep %s | awk \'{print $NF}\''%(program)
process = os.popen(com).read()

## Check for the process in the system
while process:
   process = os.popen(com).read()
   sleep(1)


## Desktop Notification
com = 'DISPLAY=:0.0 notify-send "ALERTA VIGIA:" "Terminado el proceso %s" -i gnome-terminal --hint=int:transient:1 -t 1'%(program)
try: os.system(com)
except: pass

## e-mail Notification
toaddr = 'noel.alberto.garcia@gmail.com'
body = 'Finished process: %s'%(program)
send_mail(body,toaddr,subj='VIGIA')

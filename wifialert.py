#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
  This script shows a desktop notification if the state of the network
  changes (connected or not)
  TO-DO:
  - options for sound/mute
  - options to choose sound
"""

import datetime as dt
from time import sleep,time
import os
HOME = os.getenv('HOME')


def get_state(iface=None):
   if iface == None:
      ifaces = os.popen('ls /sys/class/net/').read().split()
      ifaces.remove('lo')

   states = []
   for iface in ifaces:
      fname = '/sys/class/net/%s/operstate'%(iface)
      state = open(fname,'r').read()
      state = state.lstrip().rstrip()
      if state == 'up': states.append(True)
      elif state == 'down': states.append(False)
      elif state == 'dormant': states.append(False)
      else:
         print('Unknown state:',state)
         states.append(False)
   if any(states): return True
   else: return False


if __name__ == '__main__':
   down = "(notify-send -t 100 --urgency=low -i 'error' 'Router is down') & ogg123 /usr/share/sounds/gnome/default/alerts/bark.ogg"
   up = "(notify-send -t 100 --urgency=low -i 'terminal' 'Router is back up') &"
   
   st_old = get_state()  #True
   while not os.path.isfile(HOME+'/STOP.wifialert'):
      st = get_state()
      if st != st_old: 
         if st: os.system(up)
         else: os.system(down)
      st_old = st
      sleep(5)

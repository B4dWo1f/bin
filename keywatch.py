#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import datetime as dt
from time import sleep
from mailator import send_mail


def get_last(f='last_mail.txt'):
   """ returns in minutes the time elapsed since last sent e-mail """
   try:
      last = open(f,'r').read().lstrip().rstrip()
      last = dt.datetime.strptime(last, fmt)
      last_mail = (now()-last).total_seconds()/60
      return last_mail
   except FileNotFoundError: return 1e9


import os
HOME = os.getenv('HOME')
hostname = os.uname()[1]

## run files
fname = HOME+'/.key.log'
fmail = '/tmp/last_mail.txt'
fstop = '/tmp/STOP.mail'

## notation
now = dt.datetime.now
fmt = '%Y-%m-%d-%H:%M:%S'

## Waiting time
t0 = 1    # in seconds

## Get previous number of lines
try: n_old = len(open(fname,'r').readlines())
except FileNotFoundError: n_old = 0


for _ in range(50):
   n = len(open(fname,'r').readlines())
   if n > n_old:
      print('Ha habido cambio')
      t = get_last(f=fmail)
      print('last mail send %s minutes ago'%(t))
      if t > 2:
         print('   Sending mail')
         body = 'Someone is typing in %s:\n'%(hostname)
         body += open(fname,'r').read()
         sub = 'ALERT'
         #send_mail(body,subj=sub)
         f = open(fmail,'w')
         f.write( now().strftime(fmt) )
         f.close()
      else: print('NOT sending')   # modification, but avoiding SPAM
   else: pass  # no modification
   n_old = n
   sleep(t0)

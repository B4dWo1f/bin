#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
  Script to report unauthorized ssh logins
  TO-DO:
  - figure out permission for other users
"""

import os
import sys
import mytools as to
from mailator import send_mail
HOME = os.getenv('HOME')
here = os.path.dirname(os.path.realpath(__file__))
HOSTNAME = os.uname()[1]


try:
   T = sys.argv[1]   # Arguments to be passed from the
   IP = sys.argv[2]  # sshrc file
   Q = sys.argv[3]   #
except IndexError:
   exit()


## Current local IPs
my_IPs = os.popen('hostname -I').read().split()  # Current local IP's
whitelist = my_IPs  # complete list of trustable IP's
                    # [loca,loopback,whitelist from server...]


## loopback IPs (from /etc/hosts)
aux = open('/etc/hosts','r').read().splitlines()
for l in aux:
   try:
      if l.split()[0].split('.')[0] == '127':
         whitelist.append(l.split()[0])
   except IndexError: pass


## Get trustable ips from personal Server
try:
   user,host = open('%s/server.private'%(here),'r').read().splitlines()
   os.system('scp %s@%s:.whitelist %s/.whitelist'%(user,host,HOME))
   with open('%s/.whitelist'%(HOME),'r') as f:
      aux = f.readlines()
   for l in aux:
      whitelist.append(l.lstrip().rstrip())
except: pass  # If server is down


## Report the login/connection if needed
if IP in whitelist: pass   # Do nothing
else:   # Report
   # Unnecessary?
   #toaddr = open('%s/toaddr.private'%(here),'r').read().splitlines()[0]
   body = 'Unauthorized login @ %s.\n%s (%s) %s'%(HOSTNAME,T,IP,Q)
   subj = 'ALERTA SSH'
   send_mail(body,subj=subj)

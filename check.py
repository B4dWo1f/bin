#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import ipaddress as IP
import datetime as dt
import nmap
HOME = os.getenv('HOME')
hostname = os.uname()[1]

devices = HOME+'/.devices.info'

now = dt.datetime.now()

f = open(devices,'w')
f.write(now.strftime('%Y/%m/%d %H:%M')+'  @ %s\n'%(hostname))
f.close()

class device(object):
   def __init__(self,ip='',mac='',hostname=None,ports=[]):
      self.ip = ip
      self.mac = mac
      if hostname == None: self.hostname = 'Unknown'
      else: self.hostname = hostname
      try: self.ports = list(map(int,ports.split(',')))
      except: self.ports = []
   def __str__(self):
      msg = 'Host: %s (%s)\n'%(self.ip,self.hostname)
      msg += ' MAC: %s\n'%(self.mac)
      if len(self.ports) > 0:
         msg += 'Ports:'
         for p in self.ports:
            msg += ' %s'%(p)
         msg += '\n'
      return msg
   def save(self,fname):
      """
        Append the information of the device to a given file
      """
      f = open(fname,'a')
      f.write(self.ip+'   '+self.mac+' (%s)\n'%(self.hostname))
      f.close()


interfaces = os.popen('ifconfig -a | cut -d " " -f 1').read().split()
interfaces.remove('lo')
for I in interfaces:
   try:
      _,add,Bcast,mask = os.popen('ifconfig %s | grep "Mask:"'%(I)).read().split()
   except:
      continue
   add = add.split(':')[-1]
   mask = mask.split(':')[-1]
   net = '.'.join(add.split('.')[0:-1])+'.0/'+mask
   net = IP.IPv4Network(net)

   ## Nmap. Fast discovery of alive hosts
   nm = nmap.PortScanner()
   nm.scan(net.exploded, arguments='-n -sP')
   # Store alive IPs
   ips_file = '/tmp/devices.txt'
   with open(ips_file,'w') as f:
      f.write('\n'.join(nm.all_hosts()))
   f.close()
   alive = ' '.join( nm.all_hosts() )

   ## Extract MAC of the alive devices
   os.system('fping -c1 -f %s > /dev/null 2> /dev/null'%(ips_file))
   os.system('rm %s'%(ips_file))
   resp = os.popen('/usr/sbin/arp -n | grep -v incomplete').read()
   IPs_MACs = []
   for l in resp.splitlines()[1:]:
      ip,_,mac,_,_ = l.split()
      IPs_MACs.append((ip,mac))

   ## IP-MAC dictionary
   ipmac = dict(IPs_MACs)

   ## Deep examination of hosts
   nm = nmap.PortScanner()
   nm.scan(alive, arguments='-Pn')
   for host in nm.all_hosts():
      try: hname = nm[host]['hostnames'][0]['name']
      except KeyError: hname = nm[host]['hostname'] # for deprecated version?
      except IndexError: hname = ''
      stat = nm[host].state()
      ports = ', '.join( map(str,nm[host].all_tcp()) )
      try: a = device(ip=host,mac=ipmac[host],hostname=hname,ports=ports)
      except KeyError: a = device(ip=host,mac='',hostname=hname,ports=ports)
      a.save(devices)
      print(a)
      print('')

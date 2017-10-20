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


interfaces = os.popen('ifconfig -a | cut -d " " -f 1').read().split()
interfaces.remove('lo')
for I in interfaces:
   _,add,Bcast,mask = os.popen('ifconfig %s | grep "Mask:"'%(I)).read().split()
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
   with open(devices,'w') as f:
      f.write(now.strftime("%Y-%m-%d %H:%M:%S")+'  @  '+hostname+'\n')
      for i,m in IPs_MACs:
         f.write(i+'  '+m+'\n')
   f.close()

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
      #print('-'*80)
      print('Host: %s (%s)'%(host, hname))
      try: print('MAC:',ipmac[host])
      except KeyError: pass
      print('Open ports:',ports)
      print('')

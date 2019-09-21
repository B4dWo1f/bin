#!/usr/bin/python3
# -*- coding: UTF-8 -*-

""" OJO!!! This script requires sudo """

import sys
import os
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
try: import qrcode
except ImportError:
   msg = 'python-qrcode not found. You can install it like this:\n'
   msg += 'sudo pip3 install qrcode[pil]'
   sys.exit(msg)
import qrcode.image.svg
USER = os.getenv('USER')


## Setup the output folder
try: out = sys.argv[1]
except IndexError: out = './'
if out[-1] != '/': out += '/'
os.system('mkdir -p %s'%(out))
if not os.path.isdir(out):
   print('Destination folder does not exist and could not be created')
   exit()

## Read the network files
fol = '/etc/NetworkManager/system-connections/'
onlyfiles = [ f for f in listdir(fol) if isfile(join(fol,f)) ]
print('WARNING. I need sudo permission for reading the files in %s'%(fol))
for f in onlyfiles:
   f = os.popen('sudo cat "%s"'%(fol+f)).read()
   for l in f.splitlines():
      if 'ssid=' in l: ssid = l.split('=')[1]
      elif 'psk=' in l: pwd = l.split('=')[1]
   try: ssid,pwd
   except NameError:
      print('Error')
      print(f)
      continue
   img = qrcode.make(pwd)
   img.save('/tmp/test.png')
   img = plt.imread('/tmp/test.png')
   fig, ax = plt.subplots()
   ax.imshow(img,'Greys_r')
   ax.set_title(ssid,fontsize=30)
   ax.set_xticks([])
   ax.set_yticks([])
   #ax.set_xlabel(pwd)
   ax.set(aspect=1)
   fig.tight_layout()
   fig.savefig(out+ssid+'.png')
   print(out+ssid+'.png')
   #plt.show()
   del ssid
   del pwd

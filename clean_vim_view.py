#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
 Remove view files from vim history for deleted files
"""

import os
HOME = os.getenv('HOME')

fol = HOME + '/.vim/view'
files = os.popen('ls %s'%(fol)).read().strip().splitlines()

for f in files:
   name = f.replace('~',HOME).replace('=+','/')[:-1]
   if not os.path.isfile(name):
      com = 'rm %s'%(fol+'/'+f)
      print(com)
      os.system(com)

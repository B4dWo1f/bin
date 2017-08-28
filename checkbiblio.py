#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import sys


try: fname = sys.argv[1]
except IndexError: 
   print('No .bib file specified')
   exit()

cites = os.popen('grep "@" %s'%(fname)).read()

cites = cites.splitlines()

duplicates = set([x for x in cites if cites.count(x) > 1])

if len(duplicates) > 0:
   print('Duplicates:')
   for x in duplicates:
      print(x)
else:
   print('Congratulations!! No duplicated keys in %s'%(fname))

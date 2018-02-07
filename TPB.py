#!/usr/bin/python3
# -*- coding: UTF-8 -*-

""" Open a random PirateBay mirror from proxybay """

import os
from random import choice

tmp_list = '/tmp/list.txt'
com = 'wget https://proxybay.la/list.txt -O %s'%(tmp_list)
com += ' > /dev/null 2> /dev/null'
os.system(com)

lines = open(tmp_list,'r').readlines()
urls = []
for l in lines[3:]:
   ll = l.lstrip().rstrip()
   if len(ll) > 0: urls.append(ll)

url = choice(urls)

os.system('firefox -private-window "%s" & exit'%(url))
os.system('rm %s'%(tmp_list))


#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
HOME = os.getenv('HOME')

fol = HOME + '/'

devs = os.popen('ls /dev/video*').read().strip().splitlines()

for dev in devs:
   fname = fol + 'foto' + dev.replace('/dev/video','') + '.jpg'
   com =  'ffmpeg -v 0 -f video4linux2'
   #' -s %s'%(res)
   com += ' -i %s -ss 0:0:5 -frames 1 %s'%(dev,fname)
   os.system(com)

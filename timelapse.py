#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import sys


try: vid_name,fps, fname = sys.argv[1:]
except IndexError:
   print('Parmeters not specified')
   print('please enter:')
   print('timelapse.py video_name fps file.txtx')
   exit()

ext = open(fname,'r').readlines()[0].split('.')[-1]

com = 'mencoder -nosound -ovc lavc -lavcopts vcodec=mpeg4 -o %s '%(vid_name)
com += '-mf type=%s:fps=%s mf://@%s'%(ext,fps,fname)
os.system(com)
print(com)

#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import sys


try: vid_name,fps, fname = sys.argv[1:]
except:
   print('Parmeters not specified')
   print('please enter:')
   print('timelapse.py video_name fps file.txt')
   exit()

ext = open(fname,'r').readlines()[0].split('.')[-1]

com = f'mencoder -nosound -ovc lavc -lavcopts vcodec=mpeg4 -o {vid_name} -mf type={ext}:fps={fps} mf://@{fname}'
print(com)
os.system(com)

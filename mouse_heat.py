#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
  Script to record the position of the mouse pointer during T minutes (every t
  seconds). It requires xdotool
"""

import os
from time import sleep

T = 10 # minutes
t = 0.5   # sleep time

screen = os.popen('xrandr | grep -w connected').read().strip()
px = screen.split('primary')[1].split()[0].split('+')[0]
xs,ys = map(int,px.split('x'))

N = T*60 /t

X,Y = [],[]
for _ in range(int(N)):
   com = 'xdotool getmouselocation'
   x,y,_,_ = os.popen(com).read().split()
   X.append( int(x.split(':')[1]) )
   Y.append( int(y.split(':')[1]) )
   sleep(0.5)

import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.scatter(X,Y,edgecolor='none',alpha=0.5)
ax.set_title('Position of mouse in screen')
ax.set_xlim([0,xs])
ax.set_ylim([ys,0])
plt.show()

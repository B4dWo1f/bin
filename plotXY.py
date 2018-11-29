#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
 This script expects a 2 or 3 column file and will plot at most two columns
 against the first one.
 TO-DO, Include options:
  - order (True/False/X/Y)
  - same figure or 1 figure per file
  - choose columns
"""

import matplotlib.pyplot as plt
import numpy as np
import sys

try: fnames = sys.argv[1:]
except IndexError:
   print('File not specified')
   sys.exit(1)


for fname in fnames:
   try: M = np.loadtxt(fname,unpack=True)
   except: M = np.load(fname).transpose()
   
   X = M[0]
   inds = np.argsort(X)
   if M.shape[0] > 2:
      if M.shape[0] > 3: print('WARNING only plotting first 2 columns')
      Y1 = M[1]
      Y2 = M[2]
      X = X[inds]
      Y1 = Y1[inds]
      Y2 = Y2[inds]
   elif M.shape[0] == 2:
      Y1 = M[1]
      Y2 = []
      X = X[inds]
      Y1 = Y1[inds]
   
   fig, ax = plt.subplots()
   ax.plot(X,Y1,'o-')
   if len(Y2)>0:
      ax1 = ax.twinx()
      ax1.plot(X,Y2,'ro-')
   d = 0.05*abs(max(X) - min(X))
   ax.set_title(fname.split('/')[-1])
   ax.set_xlim((min(X)-d,max(X)+d))
ax.grid()
plt.show()

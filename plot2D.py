#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import numpy as np
from matplotlib.mlab import griddata
import matplotlib.pyplot as plt


import sys
try: fname = sys.argv[1]
except IndexError:
   print('File not specified')
   exit()


X,Y,Z = np.loadtxt(fname,unpack=True)

nx = len(X)
ny = len(Y)

xi = np.linspace(min(X),max(X),2*nx)
yi = np.linspace(min(Y),max(Y),2*ny)
zi = griddata(X,Y,Z,xi,yi)


fig, ax = plt.subplots()
ax.contourf(xi, yi, zi,cmap='viridis',alpha=0.6,zorder=10)
ax.scatter(X,Y,c=Z,s=50,cmap='viridis',edgecolors='none',zorder=0)
plt.show()

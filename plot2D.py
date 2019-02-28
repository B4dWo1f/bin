#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
 TO-DO, Include options:
 - interpolation (True/False)
 - nx,ny for interpolation
 - vmin/vmax
 - choose columns
"""
import sys
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt


try: fname = sys.argv[1]
except IndexError:
   print('File not specified')
   exit()

fx=1  # increment of points for the grid
fy=1  #
vmin=None
vmax=4

M = np.loadtxt(fname)
X = M[:,0]
Y = M[:,1]
Z = M[:,2]

nx = fx*len(X)
ny = fy*len(Y)


xi = np.linspace(min(X),max(X),nx)
yi = np.linspace(min(Y),max(Y),ny)
#zi = griddata(X,Y,Z,xi,yi)
zi = griddata((X, Y), Z, (xi[None,:], yi[:,None])) # , method='cubic')

if vmin == None: vmin = np.min(Z)
if vmax == None: vmax = np.max(Z)

fig, ax = plt.subplots()
#ax.contourf(xi,yi,zi,cmap='viridis',vmax=vmax, alpha=0.6,zorder=10)
ax.scatter(X,Y,c=Z,s=50,zorder=1) #,cmap='viridis',vmax=vmax,edgecolors='none',zorder=0)
ax.contourf(xi,yi,zi,100,alpha=0.8,zorder=10)
ax.set_xlim([np.min(X),np.max(X)])
ax.set_ylim([np.min(Y),np.max(Y)])
plt.show()

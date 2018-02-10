#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
 This script reads a 2-column file and plots the second column against the first
 one as well as the derivative of the data
"""

import numpy as np
import sys

try: fname = sys.argv[1]
except IndexError:
   print('File not specified')
   sys.exit(1)

X,Y = np.loadtxt(fname,unpack=True)

der_X = X[0:-1] + np.diff(X)/2
der_Y = np.diff(Y) * np.diff(X)


import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot(X,Y,'o-')
ax1 = ax.twinx()
ax1.plot(der_X,der_Y,'ro-')

ax1.axhline(0.0,ls='--',color='k')

ax.grid()
plt.show()


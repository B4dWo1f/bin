#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import sys


try: fnames = sys.argv[1:]
except IndexError:
   print('File not specified')
   exit()

fig, ax = plt.subplots()
for fname in fnames:
   name = '.'.join(fname.split('/')[-1].split('.')[:-1])
   M = np.loadtxt(fname,unpack=True)
   X = M[0]
   Y = M[1]
   ax.plot(X,Y,label=name)
ax.legend()
fig.tight_layout()
plt.show()

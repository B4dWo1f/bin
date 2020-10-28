#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
 Simplest code to generate linspace data
"""

import sys

ini,fin = list(map(float,sys.argv[1].split(',')))
N = int(sys.argv[2])

import numpy as np
for x in np.linspace(ini,fin,N):
   #print(x)
   print(round(x,5))

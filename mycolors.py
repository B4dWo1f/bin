#!/usr/bin/python3
# -*- coding: UTF-8 -*-


import matplotlib

cdict={'red'  : ((0.,   0,   0),(0.6,0.0,0.0),(1, 1.0, 1.0)), 'green': ((0., 0.0, 0.0),(0.4,1.0,1.0),(0.6,1.0,1.0),(1, 0.0, 0.0)), 'blue' : ((0., 1.0, 1.0),(0.4,0.0,0.0),(1, 0.0, 0.0))}
bgr = matplotlib.colors.LinearSegmentedColormap('bgr',cdict,256)


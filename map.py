#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import geoip
import argparse

parser = argparse.ArgumentParser(description='plot GPS in a Google Map')

help_msg = 'Obtain a google maps image'
parser.add_argument('-m',action='store_true', help=help_msg)
parser.add_argument('coor', nargs='*',help='List of coordinates to be plotted')

args = parser.parse_args()

## Prepare data
markers = []
for p in args.coor:
   pp = p.split(',')
   markers.append((float(pp[0]),float(pp[1])))

url = geoip.get_url(markers=markers) #,zoom=False)
print(url)
if args.m:
   geoip.get_map(url,fname='/tmp/map.png')
   import os
   os.system('eog /tmp/map.png')

#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
  This script runs over all the pictures in the given folder and scan the
exif data looking for the GPS position and stores the date-time and position
in the file positions.gps with format:
                lat,lon,date,timestamp
"""

import sys
import tools  # common library of the system
import datetime as dt
import os
USER = os.getenv('USER')
HOME = os.getenv('HOME')
hostname = os.uname()[1]
here = os.path.dirname(os.path.realpath(__file__))
cwd = os.getcwd()
import logging
log_file = cwd+'/'+'ubication.log'
here = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(level=logging.DEBUG,
                  format='%(asctime)s-%(name)-s-%(levelname)-s-%(message)s',
                  datefmt='%Y/%m/%d-%H:%M', filename=log_file, filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
fmt = logging.Formatter('%(name)s: %(levelname)s %(message)s')
console.setFormatter(fmt)
logging.getLogger('').addHandler(console)
LG = logging.getLogger('main')


## INPUT parameters
try: folder = sys.argv[1]
except IndexError: folder = './'
folder = os.path.abspath(folder)
if folder[-1] != '/': folder += '/'

outfile = 'positions.gps'


def deg2dec(deg,minu,sec):
   """ Converts degree, minute, second, to decimal """
   return deg+minu/60.+sec/3600.

def degd2dec(deg,minu,sec,d):
   """ Same as deg2dec including direction {'N','E','S','W'} """
   NSEW = {'E':1,'N':1,'S':-1,'W':-1}
   value = deg2dec(deg,minu,sec)
   sign = NSEW[d]
   return sign * value

def date2timestamp(fecha,epoch=dt.datetime(1970, 1, 1)):
   timestamp = (fecha - epoch) // dt.timedelta(seconds=1) # Integer
   return timestamp #(dt - epoch) // dt.timedelta(seconds=1)

def get_exif(fname):
   """
     Returns the GPS data: date-time, lat,lon from a given file.
     If the data is missing returns None,None,None
     ** date-time comes in UTC
   """
   RESP = os.popen('exif --ifd=GPS -m "%s"'%(f)).read()
   keys,values = [],[]
   for l in RESP.splitlines():
      ll = l.split('\t')
      keys.append(ll[0].replace(' ','_'))
      values.append(ll[1])
   GPS = dict(zip(keys, values))
   try:  # Check if all the GPS data exists
      GPS['Latitude']
      GPS['Longitude']
      GPS['North_or_South_Latitude']
      GPS['East_or_West_Longitude']
      GPS['GPS_Time_(Atomic_Clock)']
      GPS['GPS_Date']
   except KeyError: return None,None,None
   # Time
   tim = GPS['GPS_Time_(Atomic_Clock)']
   try: tim = dt.datetime.strptime(tim, '%H:%M:%S.%f').time()
   except ValueError: tim = dt.datetime.strptime(tim, '%H:%M:%S,%f').time()
   dat = GPS['GPS_Date']
   dat = dt.datetime.strptime(dat, '%Y:%m:%d').date()
   date = dt.datetime.combine(dat,tim)
   # Latitude
   aux = GPS['Latitude']
   A = [a.replace(',','.') for a in aux.split(', ')]  # for crazy local format
   deg,minu,sec = map(float,A)
   lat = degd2dec(deg,minu,sec,GPS['North_or_South_Latitude'])
   #singLA = NSEW[GPS['North_or_South_Latitude']]
   #lat = singLA*lat
   # Longitude
   aux = GPS['Longitude']
   A = [a.replace(',','.') for a in aux.split(', ')]  # for crazy local format
   deg,minu,sec = map(float,A)
   lon = degd2dec(deg,minu,sec,GPS['East_or_West_Longitude'])
   #singLO = NSEW[GPS['East_or_West_Longitude']]
   #lon = singLO*lon
   return date,lat,lon


## Start analyzing
LG.info('Analyzing folder: '+folder)
LG.info('Output file: '+os.path.abspath(outfile))

fi = open(outfile,'w')
fi.write('lat,lon,date,timestamp\n')
for f in tools.files(folder):
   if f[-4:] != '.jpg': continue
   LG.info('Photo: '+f)
   ff = f.replace('.jpg','')
   date_fmts = ['%Y-%m-%d %H.%M.%S','IMG_%Y%m%d_%H%M%S','%Y%m%d_%H%M%S']
   done = False
   i = 0
   while not done:   #XXX Why while loop???? USE for loop!!!!
      try:
         fechaa = dt.datetime.strptime(ff,date_fmts[i])
         done = True
      except ValueError: done = False
      except IndexError: done = True
      i += 1
   dat,lat,lon = get_exif(f)
   ##TODO include date checker to ensure compatibility between UTC and name
   #If the date could not be extracted from the file name, use the GPS(UTC)
   #shifted to local timezone
   try: fechaa
   except NameError:
      msg = 'Date NOT extracted from name. Using GPS date instead. '
      msg += 'Maybe timezones are being mixed'
      LG.warning(msg)
      shift_from_utc = dt.datetime.now() - dt.datetime.utcnow()
      shift_from_utc_h = round(shift_from_utc.total_seconds())/3600
      shift_from_utc = dt.timedelta(hours=shift_from_utc_h)
      fechaa = dat + shift_from_utc
   fecha = fechaa.strftime('%Y/%m/%d-%H:%M')
   if lat != None and lon != None:
      tims = date2timestamp(fechaa)
      fi.write(str(lat)+','+str(lon)+','+fecha+','+str(tims)+'\n')
      LG.info('Data: '+fecha+' '+str(lat)+' '+str(lon))
   else: LG.error(f+' No GPS data')
fi.close()
LG.info('Done.')

#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from tools import get_public_IP
from geoip import analyze_IP
import datetime as dt
from urllib.request import Request, urlopen
import json

UTCshift = dt.datetime.now() - dt.datetime.utcnow()

def make_request(url):
   """ Make http request """
   req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
   html_doc = urlopen(req).read().decode()
   return html_doc

def clean_iso8601(date):
   try: 
      date,shift = date.split('+')
      sign = 1
   except ValueError:
      date,shift = date.split('-')
      sign = -1
   finally: pass
   date = dt.datetime.strptime(date,'%Y-%m-%dT%H:%M:%S')
   h,m = map(int,shift.split(':'))
   shift = dt.timedelta(hours=h,minutes=m)
   return date+shift


import sys
try: ip = sys.argv[1]
except IndexError: ip = get_public_IP()

info = analyze_IP(ip)

lat,lon = info.coor

url = 'https://api.sunrise-sunset.org/json?lat=%s&lng=%s&date=today&formatted=0'%(lat,lon)
html_doc = make_request(url)
resp = json.loads(html_doc)
sunrise = clean_iso8601(resp['results']['sunrise'])
#print('Sunrise at:',sunrise,'UTC  //',sunrise+UTCshift,'(local time)')
print('Sunrise at:',(sunrise+UTCshift).strftime('%H:%M'),'(local time)')
sunset = clean_iso8601(resp['results']['sunset'])
#print('Sunset at:',sunset,'UTC  //',sunset+UTCshift,'(local time)')
print('Sunset at:',(sunset+UTCshift).strftime('%H:%M'),'(local time)')

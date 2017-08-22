#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
#import urllib2
from urllib.request import urlopen
from random import choice
from random import random
import json
from time import sleep


def analyze_MAC(MAC):
   """ Randomly chooses a web service to look up the MAC information """
   funcs = [macvendorlookup,macvendors]
   resp = None
   cont = 0
   while resp == None and cont < 10:
      func = choice(funcs)
      resp = func(MAC)
      cont += 1
   return resp

def macvendorlookup(MAC):
   """ Download the information from the API of macvendorlookup.com """
   url = 'http://www.macvendorlookup.com/api/v2/%s'%(MAC)
   print('Using',url)
   done,cont = False,0
   while not done and cont < 50:
      response = urlopen(url)
      page_source = response.read()
      page_source = page_source.decode('utf-8')
      page_source = page_source.replace('[','').replace(']','')
      try:
         resp = json.loads(page_source)
         done = True
         return resp['company'].title()  # Only interested in company
      except json.decoder.JSONDecodeError:
         done = False
         sleep(10*random())
      cont += 1
   return None

def macvendors(MAC):
   """ Download the information from the API of macvendors.com """
   url = 'http://api.macvendors.com/%s'%(MAC)
   print('Using',url)
   response = urlopen(url)
   page_source = response.read().decode('utf-8')
   return page_source.title()


if __name__ == '__main__':
   try: MAC = sys.argv[1]
   except IndexError: sys.exit('ERROR: No MAC specified')

   ## Prepare MAC address
   MAC = MAC.replace(':','-')
   print(analyze_MAC(MAC))

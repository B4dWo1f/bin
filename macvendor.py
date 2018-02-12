#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
#import urllib2
from urllib.request import urlopen, Request
from random import choice, seed
from random import random as rand
import json
from time import sleep


def analyze_MAC(MAC):
   """ Randomly chooses a web service to look up the MAC information """
   funcs = [macvendors, macvendors_co] #, macvendorlookup]
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
         sleep(10*rand())
      cont += 1
   return None

def macvendors(MAC):
   """ Download the information from the API of macvendors.com """
   url = 'http://api.macvendors.com/%s'%(MAC)
   response = urlopen(url)
   page_source = response.read().decode('utf-8')
   return page_source.title()

def macvendors_co(MAC):
   url = 'https://macvendors.co/api/%s'%(MAC)
   request = Request(url, headers={'User-Agent' : "API Browser"})
   response = urlopen( request )
   page_source = response.read()
   page_source = page_source.decode('utf-8')
   resp = json.loads(page_source)
   return resp['result']['company'].title()


if __name__ == '__main__':
   try: MAC = sys.argv[1]
   except IndexError: sys.exit('ERROR: No MAC specified')

   ## Prepare MAC address
   MAC = MAC.replace(':','-')
   print(analyze_MAC(MAC))

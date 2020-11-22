#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import datetime as dt
from urllib.request import Request, urlopen, urlretrieve
# import urllib.parse
from urllib.error import URLError
from bs4 import BeautifulSoup

def make_request(url):
   """ Make http request """
   req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
   out = False
   while not out:
      try:
         html = urlopen(req,timeout=30)
         out = True
      except URLError:
         # LG.error(f'URLError: {url}')
         print(f'URLError: {url}')
         out = False
   html_doc = html.read()
   try:
      charset = html.headers.get_content_charset()
      html_doc = html_doc.decode(charset, errors='ignore')
   except TypeError: html_doc = html_doc.decode()
   except: html_doc = html_doc.decode()
   return html_doc


root = 'https://apod.nasa.gov/apod'
today = dt.datetime.now()
url = f'{root}/ap{today.strftime("%y%m%d")}.html'
# print(url)
htmldoc = make_request(url)
soup = BeautifulSoup(htmldoc, 'html.parser')

title = soup.findAll('center')[1].text.splitlines()[1].strip()
# print(title)

for img in soup.findAll('img'):
   img = f"{root}/{img['src']}"
# print(img)
fimg = '/tmp/apod.jpg'
try: urlretrieve(img, fimg)
except NameError:
   print('No images today')
   exit()


text = soup.findAll('p')[2].text.split(" Tomorrow's picture:")[0].strip()
first, *text = text.splitlines()
text = ' '.join(text)
old_text = ''
while old_text != text:
   old_text = text
   text = text.replace('  ',' ')
# text = text.replace('\t',' ')
# text = text.replace('\t',' ')
# print(first)
text = ' - '.join([title,text])
text = text[:1023]   # API limit
extra = '... https://apod.nasa.gov/apod'
text = text[:-len(extra)] + extra

import sys
import os
HOME = os.getenv('HOME')
sys.path.append(f'{HOME}/bin')
import sysbot
sysbot.send_picture(fimg, text)
# print('Done!')
 
# Send also tsumego-proverb
url = 'https://tsumego-hero.com'
htmldoc = make_request(url)
soup = BeautifulSoup(htmldoc, 'html.parser')

img = soup.find('div',{'class':'homeLeft'}).find('img')['src']
img = f'{url}{img}'
try: urlretrieve(img, fimg)
except NameError:
   print('No images today')
   exit()
sysbot.send_picture(fimg, 'tsumego-hero.com')

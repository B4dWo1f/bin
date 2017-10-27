#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import string
from random import choice, seed, randint, getrandbits, random

def passwrd(pwdSize=8):
   """ Generates a random string of letters and digits with pwdSize length """
   ## all possible letters and numbers
   chars = string.ascii_letters + string.digits
   return ''.join((choice(chars)) for x in range(pwdSize))

def maze(steps=3,folder='/tmp/',hid=True):
   """
     Returns the path for a folder behind ${steps} folders.
     hid: makes all the folders hidden
     DOES NOT CREATE THE PATH
   """
   for _ in range(steps):
      if hid: h = '.'
      else: h = ''
      folder += h+passwrd(randint(3,6))+'/'
   return folder

def create_maze(final,n=6):
   """
     Creates a maze around a final location. Runs over the (final) path
     creating extra folders at each step to hide the content.
     n = max number of empty folders per directory
   """
   com = 'mkdir -p %s'%(final)  # Create target folder
   os.system('mkdir -p %s'%(final))  # Create target folder
   list_folders = final.split('/')[2:-1]
   current = '/'+final.split('/')[1]+'/'
   for fol in list_folders:
      current += fol+'/'
      h = hid=bool(getrandbits(1))
      if current != final: lio = maze(randint(2,n),folder=current,hid=h)
      os.system('mkdir -p %s'%(lio))

def full_disguise(word,chance=1):
   """
     Apply all possible modifications
   """
   aux = disguise(word.lower(),chance=random())
   return rand_capital(aux,chance=random())

def disguise(word,chance=1):
   """
     Replace letters by numbers. chance determines how many of the changeable
     letter will be changed (0 <= chance <= 1)
   """
   word2num = {'a':4,'e':3,'i':1,'o':0,'t':7,'l':1,'s':5,'&':8,
               4:'a',3:'e',1:'i',0:'o',7:'t',1:'l',5:'s',8:'&'}
   changed = ''
   for l in word:
      try:
         n = word2num[l]
         if random() <= chance: changed += str(n)
         else: changed += l
      except KeyError: changed += l
   return changed

def rand_capital(word,chance=0.5):
   """
     toggle the case of the letters. chance determines how many of the
     changeable characters will be changed (0 <= chance <= 1)
   """
   def toggle_case(l):
      if l.isupper(): return l.lower()
      elif l.islower(): return l.upper()
      else: return l
   changed = ''
   for l in word:
      if random() <= chance: changed += toggle_case(l)
      else: changed += l
   return changed

def add_number(word,n=4):
   """ Add a string of n random numbers to the given word """
   return word + ''.join( [str(randint(0,9)) for _ in range(n)] )

if __name__ == '__main__':
   import sys
   try: fname = sys.argv[1]
   except IndexError:
      print('String not specified. Here\'s a random string of characters')
      print(passwrd(randint(5,10)))
      exit()
   
   print('Disguising:',fname)
   print(full_disguise(fname))

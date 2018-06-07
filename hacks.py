#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import string
import numpy as np
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

def from_dictionary(words,add_num=True,size=(6,8),shuf=False,maxlen=1e5):
   """ 
     create all the combinations of letters and numbers from a list of words
   """
   all_variations = []
   letters = ''.join(words)
   letters = list(set(letters))
   letters = ''.join(letters)
   if add_num: letters += '0123456789'
   for r in range(size[0],size[1]+1):
      for i in combinations(letters, r):
         all_variations.append(''.join(i))
         if len(all_variations) > maxlen: break
   if shuf: shuffle(all_variations)
   return all_variations

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


us_US = {'q':(0,1),'w':(0,2),'e':(0,3),'r':(0,4),'t':(0,5),'y':(0,6),'u':(0,7),
         'i':(0,8),'o':(0,9),'p':(0,10),
         'a':(1,1),'s':(1,2),'d':(1,3),'f':(1,4),'g':(1,5),'h':(1,6),'j':(1,7),
         'k':(1,8),'l':(1,9),
         'z':(2,1),'x':(2,2),'c':(2,3),'v':(2,4),'b':(2,5),'n':(2,6),'m':(2,7)}

es_ES = {'q':(0,1),'w':(0,2),'e':(0,3),'r':(0,4),'t':(0,5),'y':(0,6),'u':(0,7),
         'i':(0,8),'o':(0,9),'p':(0,10),
         'a':(1,1),'s':(1,2),'d':(1,3),'f':(1,4),'g':(1,5),'h':(1,6),'j':(1,7),
         'k':(1,8),'l':(1,9),'ñ':(1,10),
         'z':(2,1),'x':(2,2),'c':(2,3),'v':(2,4),'b':(2,5),'n':(2,6),'m':(2,7)}

pt_PT = {'q':(0,1),'w':(0,2),'e':(0,3),'r':(0,4),'t':(0,5),'y':(0,6),'u':(0,7),
         'i':(0,8),'o':(0,9),'p':(0,10),
         'a':(1,1),'s':(1,2),'d':(1,3),'f':(1,4),'g':(1,5),'h':(1,6),'j':(1,7),
         'k':(1,8),'l':(1,9),'ç':(1,10),
         'z':(2,1),'x':(2,2),'c':(2,3),'v':(2,4),'b':(2,5),'n':(2,6),'m':(2,7)}


keyboard = {'es':es_ES, 'en':us_US, 'pt':pt_PT}

def closest_key(letter,keybd=keyboard['en'],d=1.0):
   """
     Returns the closest key in a QWERTY keyboard to a given letter
   """
   closest = []
   for a in keybd:
      if a != letter:
         dist = distance(letter,a,keybd=keybd)
         if dist <= d: closest.append(a)
   return closest


def distance(letter1,letter2,keybd=keyboard['en']):
   """
     Returns the distance between two letters in a QWERTY keyboard
   """
   P = np.array(keybd[letter1])
   Q = np.array(keybd[letter2])
   return np.linalg.norm(P-Q)

def score(str1,str2,keybd=keyboard['en']):
   """
     Returns the coincidence score between two strings
   """
   maxdist = distance('p','z')
   str1 = str1.replace(' ','')
   str2 = str2.replace(' ','')
   eq = 0
   for c1,c2 in zip(str1,str2):
      if c1 == c2: eq += 1
      else:
         if c2 in closest_key(c1):
            eq += 1-distance(c1,c2)/maxdist
   tot = len(str1)
   return eq/float(tot)


if __name__ == '__main__':
   import sys
   try: fname = sys.argv[1]
   except IndexError:
      print('String not specified. Here\'s a random string of characters')
      print(passwrd(randint(5,10)))
      exit()
   
   print('Disguising:',fname)
   print(full_disguise(fname))


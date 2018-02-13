#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
  Behaviour:
  - If ONLY a rar file is specified, then try to uncompress it by guessing
                                                         the pass (brute force)
  - If a random file (not .rar) or a set of files is provided then compress
                                               the file(s) in a protected file.
  TO-DO:
  - loggin
  - parser options
"""


from mailator import send_mail
import string
from random import randint
import hacks
import sys
import os


def compress(fname,password,comprfname=None):
   """ compress file fname with some password """
   if comprfname != None: comprfname = fname
   os.system('rar a -hp%s %s %s'%(password,comprfname,fname))


def decompress(fname,pwrd):
   return os.popen('unrar e -hp%s %s 2> /dev/null'%(guess,fname)).read()


def brute_force_file(fname,maxindex=None):
   """ Brute force decompression of a rar file """
   if maxindex == None: maxindex = 8
   tried = []
   cont = 0
   done = False
   while not done:
      guess = hacks.passwrd(randint(4,maxindex))
      i = 0
      while guess in tried:
           guess = hacks.passwrd(randint(4,maxindex))
           i += 1
      resp = decompress(fname,guess)
      if "All OK" in resp:
         print('='*80)
         print('DONE after %s tries!!!'%(cont))
         print('     The password is: %s'%(guess))
         print('='*80)
         done = True
      elif "Total errors:" in resp:
         done = False
      cont += 1
      if cont%100 == 0 : print('%s Intentos. Current pass:'%(cont),guess)
      tried.append(guess)


def checkfile(fil):
   """" Checks if a given file exists or not """
   if os.path.isfile(fil): return True
   else: return False


if __name__ == '__main__':
   try: fname = sys.argv[1]
   except IndexError:
      print('File(s) not specified.')
      sys.exit()

   if fname[-4:] == '.rar': ######################################## Uncompress
      brute_force_file(fname)
   elif fname[-4:] != '.rar' or len(sys.argv) > 2: ################### Compress
      password = sys.argv[2]
      compress(fname,password)

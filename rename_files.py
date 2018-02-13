#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
 This scripts merges and renames all the files in several folders into another
 one.
  folders: source of files
  out_folder: target folder (it will contain all the files previously in
              contained in folders)
  root_name: New name for the files (IMG_01.jpg...)
  TO-DO:
  - fix for . and .. notation
"""

## LOG #########################################################################
import logging
logging.basicConfig(level=logging.DEBUG,
                  format='%(asctime)s %(name)s:%(levelname)s - %(message)s',
                  datefmt='%Y/%m/%d-%H:%M:%S',
                  filename='renamer.log', filemode='w')
## Console Handler
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
fmt = logging.Formatter('%(name)s -%(levelname)s- %(message)s')
sh.setFormatter(fmt)
#logging.getLogger('').addHandler(console)
LG = logging.getLogger('main')
LG.addHandler(sh)
################################################################################

## Options #####################################################################
import argparse
parser = argparse.ArgumentParser(description='Main parser')
parser.add_argument('-i',nargs='*',type=str, help='Folders to merge')
parser.add_argument('-o',nargs=1,type=str,default='./',help='Output folder')
parser.add_argument('-r',nargs=1,type=str,default='IMG_',
                                                    help='Root name for files')
parser.add_argument('-l',nargs=1,type=int,default=4,
                                             help='Length of numbers in names')
args = parser.parse_args()
################################################################################


## Parsing options
folders = args.i
out_folder = args.o[0]
root_name = args.r[0]
l = args.l
print(folders)
print(out_folder)
print(root_name)
print(l)
print('-------------')


from tools import files
import sys
import os
USER = os.getenv('USER')
HOME = os.getenv('HOME')
hostname = os.uname()[1]
here = os.path.dirname(os.path.realpath(__file__))
cwd = os.getcwd() + '/'   # Folder were ths script is executed


## Clean folder names
for i in range(len(folders)):
   folders[i] = cwd + folders[i]
   if folders[i][-1] != '/': folders[i] += '/'
if out_folder[-1] != '/': out_folder = cwd + out_folder + '/'


## Check/Create the output folder
if not os.path.isdir(out_folder):
   com = 'mkdir -p %s'%(out_folder)
   LG.info('sys: '+com)
   os.system(com)
else:  # Output folder already exists
   LG.warning('The output folder (%s) already exists.'%(out_folder))
   out_files = files(out_folder)
   n = len(out_files)
   if n > 0:
      warn = 'The output folder is not empty'
      LG.warning(warn)
      r= input(warn+'\nUse this folder anyway?(Y/n)\n')
      if r == 'Y': LG.info('Using pre-existing folder %s'%(out_folder))
      else:
         LG.critical('Output folder already contains files.')
         exit()
   else: LG.warning('Empyt output folder')


## Rename files
cont = 0
for f in folders:
   LG.info('Processing fodler '+f)
   all_files = files(f,abspath=True)
   all_files = sorted(all_files)
   LG.debug('%s files to be copied'%(len(all_files)))
   for fil in all_files:
      #name = '.'.join( a.split('.')[0:-1] )
      ext = '.' + fil.split('.')[-1]
      name = out_folder + root_name + '%04d'%(cont) + ext
      num = '{num:0{width}}'.format(num=cont, width=l)
      msg = '%s ---> %s'%(fil.replace(cwd,''),name.replace(cwd,''))
      LG.info(msg)
      com = 'cp %s %s'%(fil,out_folder+root_name+'%04d'%(cont)+ext)
      LG.debug(com)
      os.system(com)
      cont += 1

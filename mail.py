#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from mailator import send_mail
import argparse

parser = argparse.ArgumentParser(description='Main parser')
parser.add_argument('-d',nargs='*',type=str, default=[],
                    help='List of e-mail addresses to send the files to')
parser.add_argument('-f',nargs='*',type=str, default=None,
                    help='List of files to be send')
parser.add_argument('-b',nargs=1,type=str,default='',help='Body of the e-mail')
parser.add_argument('-s',nargs=1,type=str,default='',
                    help='Subject of the e-mail')
parser.add_argument('rest', nargs='*')

args = parser.parse_args()



#### Parse input options
## Attached files
if isinstance(args.f,list): lista = args.f + args.rest
else: lista = args.rest
att = [l for l in lista if l is not None]

## Dest address
toaddr = []
for x in args.d:
   if len(x.split('@')) != 2: parser.print_help()
   else:
      if len(x.split('@')[1].split('.')) >= 2: toaddr.append(x)
      else: parser.print_help()

## Body of e-mail
if isinstance(args.b,list): body = '\n'.join(args.b)
else: body = 'Here you have the file ;)'

## Subject of e-mail
if isinstance(args.s,list): subj = '\n'.join(args.s)
else: subj = 'Your File'


#### Send e-mail
if len(toaddr) == 0: send_mail(body,subj=subj,att=att)
else: send_mail(body,toaddr,subj=subj,att=att)

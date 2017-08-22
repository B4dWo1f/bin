#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from mailator import send_mail
import argparse

parser = argparse.ArgumentParser(description='Main parser')
parser.add_argument('-d',nargs='*',type=[], default=[],
                    help='List of e-mail addresses to send the files to')
parser.add_argument('-f',nargs='*',type=[], default=[None],
                    help='List of files to be send')
parser.add_argument('-b',nargs=1,type=str,default='',help='Body of the e-mail')
parser.add_argument('rest', nargs='*')


args = parser.parse_args()
lista = args.f + args.rest
toaddr = args.d

att = [l for l in lista if l is not None]
if len(args.b[0]) == 0: body = 'Here you have the file ;)'
else: body = args.b[0]
subj = 'Your File'
if len(toaddr) == 0: send_mail(body,subj=subj,att=att)
else: send_mail(body,toaddr,subj=subj,att=att)

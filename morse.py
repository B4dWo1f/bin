#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
 Script to translate into/from morse
 ./morse.py "hola"
 ./morse.py -r ".... --- .-.. .-"
"""

import sys 
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-r',action='store_true', help='From morse')
parser.add_argument('rest', nargs='*')
args = parser.parse_args()


CODE = {'A': '.-',     'B': '-...',   'C': '-.-.', 
        'D': '-..',    'E': '.',      'F': '..-.',
        'G': '--.',    'H': '....',   'I': '..',
        'J': '.---',   'K': '-.-',    'L': '.-..',
        'M': '--',     'N': '-.',     'O': '---',
        'P': '.--.',   'Q': '--.-',   'R': '.-.',
        'S': '...',    'T': '-',      'U': '..-',
        'V': '...-',   'W': '.--',    'X': '-..-',
        'Y': '-.--',   'Z': '--..',
        '0': '-----',  '1': '.----',  '2': '..---',
        '3': '...--',  '4': '....-',  '5': '.....',
        '6': '-....',  '7': '--...',  '8': '---..',
        '9': '----.'}

CODE_REVERSED = {value:key for key,value in CODE.items()}

def to_morse(s): return ' '.join(CODE.get(i.upper()) for i in s)

def from_morse(s): return ''.join(CODE_REVERSED.get(i) for i in s.split())

words = args.rest

if args.r:
   for word in words:
      print(from_morse(word))
else:
   for word in words:
      print(to_morse(word))

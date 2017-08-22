#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import tools as to
import os
HOME = os.getenv('HOME')

if to.internet(): # Check if there is internet
   torrents = to.files('%s/.config/transmission/torrents/'%(HOME))
   if len(torrents) > 0:
      os.system('nohup transmission-gtk > /dev/null 2> /dev/null &')


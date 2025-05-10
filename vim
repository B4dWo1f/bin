#!/bin/bash

#
# In Ubuntu 24.04 /usr/bin/resize is not present
# for this script to work it requires xterm
#   $ sudo apt-get install xterm
#

if [[ $1 == *.py ]]; then
   # Resize the window to give extra room for the line numbers and keep the 80
   # columns
   source <(/usr/bin/resize -s)
   EXTRA=`wc -l "$@" 2> /dev/null | cut -d " " -f 1`  # width of column number
   EXTRA=`echo ${#EXTRA}`
   ORIGINAL_WIDTH=$COLUMNS
   WIDTH=$(($COLUMNS + EXTRA + 3))
   /usr/bin/resize -s $LINES $WIDTH > /dev/null 2> /dev/null
   /usr/bin/vim "$@"
   /usr/bin/resize -s $LINES $ORIGINAL_WIDTH > /dev/null 2> /dev/null
else
   /usr/bin/vim "$@"
fi

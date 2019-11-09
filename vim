#!/bin/bash

if [[ $1 == *.py ]]; then
   # Resize the window to give extra room for the line numbers and keep the 80
   # columns
   source <(/usr/bin/resize -s)
   EXTRA=`wc -l "$@" | cut -d " " -f 1 2> /dev/null`
   EXTRA=`echo ${#EXTRA}`
   WIDTH=$(($COLUMNS + EXTRA + 2))
   /usr/bin/resize -s $LINES $WIDTH > /dev/null 2> /dev/null
   /usr/bin/vim "$@"
   /usr/bin/resize -s $LINES $COLUMNS > /dev/null 2> /dev/null
else
   /usr/bin/vim "$@"
fi

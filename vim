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
elif [[ $1 == *.tex ]]; then
   # Resize window and place to the right most side
   WINDOW_ID=`xwininfo -id $(xdotool getactivewindow) | grep "Window id:" | awk '{print $4}'`
   X0=`xwininfo -id $(xdotool getactivewindow) | grep "Absolute upper-left X:" | awk '{print $4}'`
   Y0=`xwininfo -id $(xdotool getactivewindow) | grep "Absolute upper-left Y:" | awk '{print $4}'`
   SCREEN=`xrandr | grep ' connected primary ' | awk '{print $4}' | cut -d "x" -f 1`
   source <(/usr/bin/resize -s)
   /usr/bin/resize -s 46 $COLUMNS > /dev/null 2> /dev/null
   xdotool windowmove $WINDOW_ID $SCREEN 0  # move to extrem (max allowed)
   /usr/bin/vim "$@"
   /usr/bin/resize -s $LINES $COLUMNS > /dev/null 2> /dev/null
   xdotool windowmove $WINDOW_ID $X0 $Y0  # move to extrem (max allowed)
else
   /usr/bin/vim "$@"
fi

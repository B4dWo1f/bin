#!/bin/bash

RUNNING=`ps -e | grep -w logkeys`

if [[ -z $RUNNING ]] ; then
   echo "STARTING logkeys"
   sudo logkeys -m $HOME/.logkeys/maps/en_US.map -o $HOME/log.txt -s
else
   echo "STOPPING logkeys"
   sudo logkeys -k
fi


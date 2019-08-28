#!/bin/bash

RUNNING=`ps -e | grep -w logkeys`
FILE=$HOME/.log.txt

touch $FILE
if [[ -z $RUNNING ]] ; then
   echo "STARTING logkeys"
   sudo logkeys -m $HOME/.logkeys/maps/en_US.map -o $FILE -s
else
   echo "STOPPING logkeys"
   sudo logkeys -k
fi


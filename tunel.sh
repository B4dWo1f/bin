#!/bin/bash

#
#  Checks if the tunnel is active by checking the preciously stored port
# if the tunnel is not ready, establishes a new connection.
# Generates a "spam" file containing the last used port at $HOME/.tunnel
#
# You need to have a passwordless connection to the server such that
#         ssh -p $SSH_PORT $SSH_USER@$SSH_IP
# should work automatically. [if you don't know how, check ssh-copy-id]
#

## Local side
FILE="$HOME/.tunnel"  # File to store the previous port
OLD_PORT=`cat $FILE`
LOCAL_USER=$USER

## Server side
SSH_PORT=22                     # Port for ssh in the server
SSH_USER="noel"                 # User at the server
SSH_IP="kasterborous.ddns.net"  # Server domain

PROCESS=`ps -ef | grep $OLD_PORT | grep -v grep`  # Check for the process
if [ ! "$PROCESS" ]; then
   PORT=$((RANDOM%1500+9000))    # Choose new random port

   # Make passive ssh reversed tunnel
   ssh -fN -R $PORT:localhost:$SSH_PORT $SSH_USER@$SSH_IP

   # Report command to connect from server to local
   echo "ssh -p $PORT $LOCAL_USER@localhost" > /tmp/command.txt
   echo $PORT > $FILE
   NAME=$HOSTNAME.ssh
   scp /tmp/command.txt $SSH_USER@$SSH_IP:$NAME

   rm /tmp/command.txt  # Clean temporary files
fi

#!/bin/bash

#
#   This script changes the file extensions to lowercase.
# If an especific extension is provided it will only change those files
# if no extension is provided it will change all files in the folder
# WARNING: this action may overwrite files
#

if [ -z $1 ]; then
   echo "all files"
   find . -iname "*.*" -exec sh -c 'a=$(echo "$0" | sed -r "s/([^.]*)\$/\L\1/"); [ "$a" != "$0" ] && mv "$0" "$a" ' {} \;
else
   echo "only $1"
   find . -iname "*.$1" -exec sh -c 'a=$(echo "$0" | sed -r "s/([^.]*)\$/\L\1/"); [ "$a" != "$0" ] && mv "$0" "$a" ' {} \;
fi

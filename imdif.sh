#!/bin/bash

# Get base64 encoded image
IMG1="$(cat $1 | base64)"
IMG2="$(cat $2 | base64)"

#See if the images are the same
if [ "$IMG1" == "$IMG2" ]; then
    echo "The images are the same! Yaaaaaaaaaay!"
else
    echo "The images are different! Bleh.."
fi

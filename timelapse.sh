#!/bin/bash

echo "mencoder -nosound -ovc lavc -lavcopts vcodec=mpeg4 -o $1 -mf type=png:fps=$2 mf://@$3"

#!/bin/bash

FILE="/run/systemd/shutdown/scheduled"

if [[ -f "$FILE" ]]; then
   date -d @`cat $FILE | head -n 1 | cut -c6-15`
fi

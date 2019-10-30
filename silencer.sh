#!/bin/bash

acpi_listen | while IFS= read -r line;
do
    if [ "$line" = "jack/headphone HEADPHONE plug" ]
    then
       amixer -D pulse set Master mute
       notify-send "headphones connected. Sound is muted"
    elif [ "$line" = "jack/headphone HEADPHONE unplug" ]
    then
       amixer -D pulse set Master mute
       notify-send "headphones disconnected.  Sound is muted"
    fi
done

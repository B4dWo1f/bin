#!/bin/bash

# Wait for internet connection
while ! ping -c 1 -W 1 8.8.8.8; do
    sleep 1
done

target="$HOME/.config/transmission/torrents/"
if find "$target" -mindepth 1 -print -quit 2>/dev/null | grep -q .; then
    nohup transmission-gtk > /dev/null 2> /dev/null &
fi

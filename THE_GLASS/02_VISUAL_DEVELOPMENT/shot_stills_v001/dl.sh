#!/bin/bash
# usage: dl.sh < "index url" lines ; saves SH_<index>.png and a 4-up preview sheet
mkdir -p stills prev
while read i u; do curl -s -o stills/SH_$i.png "$u"; ffmpeg -nostdin -v error -y -i stills/SH_$i.png -vf scale=480:-1 prev/SH_$i.jpg; done

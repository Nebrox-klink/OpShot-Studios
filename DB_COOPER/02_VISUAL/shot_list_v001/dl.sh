#!/bin/bash
# usage: dl.sh ID URL  -> stills/SH_ID.png + final_jpg/SH_ID.jpg (1280 px review copy)
cd "$(dirname "$0")"
curl -sS -o stills/SH_$1.png "$2" && ffmpeg -v error -y -i stills/SH_$1.png -vf scale=1280:-2 -q:v 3 final_jpg/SH_$1.jpg && echo "SH_$1 ok"

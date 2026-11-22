#!/bin/bash
# usage: sheet.sh OUT ID ID ... -> labelled 2-column contact sheet of final_jpg/SH_ID.jpg at 640 px per tile
cd "$(dirname "$0")"; out=$1; shift; args=""; fc=""; n=0
for i in "$@"; do args="$args -i final_jpg/SH_$i.jpg"; fc="$fc[$n]scale=640:-2,drawtext=text=$i:x=8:y=8:fontsize=26:fontcolor=yellow:box=1:boxcolor=black[v$n];"; n=$((n+1)); done
lay=""; ins=""; for k in $(seq 0 $((n-1))); do lay="$lay${lay:+|}$(( (k%2)*640 ))_$(( (k/2)*360 ))"; ins="$ins[v$k]"; done
ffmpeg -v error -y $args -filter_complex "${fc}${ins}xstack=inputs=$n:layout=$lay:fill=black" "$out"

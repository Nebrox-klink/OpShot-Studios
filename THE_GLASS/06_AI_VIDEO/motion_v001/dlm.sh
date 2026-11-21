#!/bin/bash
# usage: dlm.sh <<< "index url" ; downloads clip and builds a 3-frame QC row
while read i u; do curl -s -o clips/M_$i.mp4 "$u"; for t in 0.2 2.5 4.8; do ffmpeg -nostdin -v error -y -ss $t -i clips/M_$i.mp4 -frames:v 1 -vf scale=320:-1 qc/M_${i}_$t.jpg; done; ffmpeg -nostdin -v error -y -i qc/M_${i}_0.2.jpg -i qc/M_${i}_2.5.jpg -i qc/M_${i}_4.8.jpg -filter_complex "[0][1][2]hstack=3,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='$i':x=6:y=6:fontsize=20:fontcolor=yellow:box=1:boxcolor=black" qc/row_$i.jpg; done

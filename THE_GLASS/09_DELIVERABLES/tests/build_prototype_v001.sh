#!/usr/bin/env bash
# Assemble prototype v001 (03:30–03:57): 2D SH-028→030 (20 s) + 3D SH-031 (7 s) + TEMP audio.
# Usage: build_prototype_v001.sh <nb_frames_dir> <sh031_frames_dir> <audio_mix_wav>
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
NB="$1"; F3D="$2"; MIX="$3"
FONT_TC=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf
FONT_SUB="$ROOT/03_2D_ASSETS/typography/eb-garamond-latin-500-normal.woff"
TMP="$(mktemp -d)"

# 3D preview: 960x540 EEVEE → 1280x720, gentle vignette + grain to sit with the 2D grade
ffmpeg -y -loglevel error -framerate 24 -i "$F3D/SH-031_%04d.png" \
  -vf "scale=1280:720:flags=lanczos,vignette=angle=PI/5,noise=alls=5:allf=t,format=yuv420p" \
  -c:v libx264 -crf 18 -preset slow -movflags +faststart "$ROOT/05_BLENDER/renders/SH-031_preview_v001.mp4"

# picture: 2D (480 f) + 3D (168 f) = 648 f = 27.0 s
ffmpeg -y -loglevel error -framerate 24 -i "$NB/SH-028-030_%04d.png" -i "$ROOT/05_BLENDER/renders/SH-031_preview_v001.mp4" \
  -filter_complex "[0:v]format=yuv420p,setsar=1[a];[1:v]setsar=1[b];[a][b]concat=n=2:v=1:a=0[v]" -map "[v]" \
  -c:v libx264 -crf 18 -preset slow "$TMP/picture.mp4"

# CLEAN version (no burn-ins)
ffmpeg -y -loglevel error -i "$TMP/picture.mp4" -i "$MIX" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest \
  -movflags +faststart "$ROOT/09_DELIVERABLES/tests/THE_GLASS_prototype_v001_0330-0357.mp4"

# REVIEW version: shot IDs, 2D/3D tag, film timecode and TEMP VO subtitles burnt in
lab() { echo "drawtext=fontfile=$FONT_TC:text='$1':x=24:y=20:fontsize=22:fontcolor=white@0.9:box=1:boxcolor=$2@0.75:boxborderw=8:enable='between(t,$3,$4)'"; }
sub() { echo "drawtext=fontfile=$FONT_SUB:text='$1':x=(w-tw)/2:y=h-70:fontsize=30:fontcolor=white:box=1:boxcolor=black@0.55:boxborderw=10:enable='between(t,$2,$3)'"; }
VF="$(lab 'SH-028  ·  2D ANIMATION' 0x284e6e 0 7),$(lab 'SH-029  ·  2D ANIMATION' 0x284e6e 7 14),$(lab 'SH-030  ·  2D ANIMATION' 0x284e6e 14 20),$(lab 'SH-031  ·  3D CINEMATIC 1 · Through the Glass' 0xa95149 20 27)"
VF="$VF,$(sub 'Here is the part most people don’t know.' 0.7 4.2),$(sub 'The fifth of April was not the first time they came for NOKAS.' 7.5 12.8),$(sub 'Two months earlier, Toska was already inside the courtyard.' 14.3 19.2)"
VF="$VF,drawtext=fontfile=$FONT_TC:text='TEMP VO (TTS) · PROTOTYPE v001 · 03\\:30\\:00 +%{pts\\:hms}':x=w-tw-20:y=24:fontsize=18:fontcolor=white@0.8:box=1:boxcolor=black@0.5:boxborderw=6"
ffmpeg -y -loglevel error -i "$TMP/picture.mp4" -i "$MIX" -vf "$VF" -map 0:v -map 1:a -c:v libx264 -crf 20 -preset slow \
  -c:a aac -b:a 192k -shortest -movflags +faststart "$ROOT/09_DELIVERABLES/reviews/THE_GLASS_prototype_v001_REVIEW.mp4"
rm -rf "$TMP"
echo "done"

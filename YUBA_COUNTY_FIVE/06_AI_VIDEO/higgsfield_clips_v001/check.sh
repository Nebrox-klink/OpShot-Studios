#!/bin/bash
# Usage: ./check.sh ID URL [ID URL ...]  -> clips/H_<ID>.mp4 (audio stripped) + checks/H_<ID>.jpg (first | middle | last frame, 960 px each)
cd "$(dirname "$0")" && mkdir -p clips checks
while [ $# -ge 2 ]; do
  curl -s -o /tmp/claude-0/-home-user-OpShot-Studios/b8b3a2e5-2a6b-5e55-8218-5a449dfff4ca/scratchpad/raw.mp4 "$2"
  ffmpeg -loglevel error -y -i /tmp/claude-0/-home-user-OpShot-Studios/b8b3a2e5-2a6b-5e55-8218-5a449dfff4ca/scratchpad/raw.mp4 -an -c:v copy "clips/H_$1.mp4"
  d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "clips/H_$1.mp4")
  ffmpeg -loglevel error -y -i "clips/H_$1.mp4" -vf "select='eq(n\,0)+eq(n\,60)+eq(n\,115)',scale=960:-1,tile=3x1" -frames:v 1 "checks/H_$1.jpg"
  echo "H_$1 ${d}s"; shift 2
done

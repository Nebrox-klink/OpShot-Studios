#!/bin/bash
# Usage: ./dl.sh ID URL [ID URL ...]  -> stills/SH_<ID>.png
cd "$(dirname "$0")" && mkdir -p stills
while [ $# -ge 2 ]; do curl -s -o "stills/SH_$1.png" "$2" && echo "SH_$1 $(stat -c%s stills/SH_$1.png)"; shift 2; done

#!/usr/bin/env bash
# THE GLASS: Cycles GPU test render on a rented Linux GPU machine (Spheron, Ubuntu).
# Needs ~/glass_test_bundle.tgz (uploaded from the laptop, see SPHERON_TEST.md).
# Renders 5 frames of SH-052 ("the glass gives") at 1920x1080 with real refractive glass,
# times every frame, and packs everything into ~/glass_test_results.tgz.
set -euo pipefail

SAMPLES="${SAMPLES:-128}"
FRAMES="${FRAMES:-1,60,120,180,240}"
WORK="$HOME/glass_test"
SUDO=""; [ "$(id -u)" -ne 0 ] && SUDO="sudo"

echo "== GPU"
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv || echo "WARNING: nvidia-smi not found - is this a GPU machine?"

echo "== system packages"
$SUDO apt-get update -qq
$SUDO apt-get install -y -qq wget xz-utils libxi6 libxxf86vm1 libxfixes3 libxrender1 libgl1 libegl1 \
    libxkbcommon0 libsm6 libice6 >/dev/null

mkdir -p "$WORK"; cd "$WORK"
echo "== Blender"
URL=""
for V in 5.0.1 5.0.0 4.5.3; do
  MAJ="${V%.*}"
  CAND="https://download.blender.org/release/Blender${MAJ}/blender-${V}-linux-x64.tar.xz"
  if wget -q --spider "$CAND"; then URL="$CAND"; break; fi
done
[ -n "$URL" ] || { echo "Could not find a Blender download"; exit 1; }
echo "downloading $URL"
wget -q "$URL"
tar xf "$(basename "$URL")"
BL="$WORK/$(basename "$URL" .tar.xz)/blender"
"$BL" --version | head -1

echo "== project files"
tar xzf "$HOME/glass_test_bundle.tgz" -C "$WORK"
cd "$WORK/THE_GLASS/05_BLENDER"

echo "== build the SH-052 scene (no render)"
"$BL" -b -P scripts/tg3d_courtyard_shots.py -- --shot SH-052 --out "$WORK/out" \
      --res 1920x1080 --samples 64 --step 1 --render none

echo "== Cycles test render: frames $FRAMES, $SAMPLES samples"
START=$(date +%s)
"$BL" -b -P cycles_test/cycles_glass_upgrade.py -- --blend "$WORK/out/SH-052_v001.blend" \
      --out "$WORK/results" --frames "$FRAMES" --samples "$SAMPLES" --res 1920x1080 2>&1 | grep -v "^Fra:"
END=$(date +%s)
echo "total render wall time: $((END-START)) s" | tee "$WORK/results/wall_time.txt"
nvidia-smi --query-gpu=name --format=csv,noheader > "$WORK/results/gpu.txt" 2>/dev/null || true

cd "$WORK"
tar czf "$HOME/glass_test_results.tgz" results
echo "== DONE: ~/glass_test_results.tgz"
cat "$WORK/results/timing.json"

"""Rebuild the 1080p rough cut from the normalised shot clips (Windows / macOS / Linux).

Use this on the laptop after `git pull`. It needs only Python 3 and ffmpeg on PATH.
  python 09_DELIVERABLES\\assemble_from_shots.py
Reads  09_DELIVERABLES/roughcut_v001/roughcut_manifest.csv, shots/*.mp4, THE_GLASS_roughcut_v001_mix_TEMP.flac
Writes 09_DELIVERABLES/roughcut_v001/THE_GLASS_roughcut_v001_1080p.mp4
"""
import csv
import os
import pathlib
import shutil
import subprocess

D = pathlib.Path(__file__).resolve().parent / "roughcut_v001"
FF = shutil.which("ffmpeg") or "ffmpeg"
rows = list(csv.DictReader(open(D / "roughcut_manifest.csv", encoding="utf-8")))
seen = []
for r in rows:
    if r["clip"] not in seen:
        seen.append(r["clip"])
lst = D / "concat_local.txt"
with open(lst, "w", encoding="utf-8") as fh:
    for c in seen:
        fh.write(f"file '{(D / c).as_posix()}'\n")
out = D / "THE_GLASS_roughcut_v001_1080p.mp4"
cmd = [FF, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
       "-i", str(D / "THE_GLASS_roughcut_v001_mix_TEMP.flac"), "-map", "0:v", "-map", "1:a",
       "-vf", "scale=1920:1080:flags=lanczos,format=yuv420p", "-c:v", "libx264", "-crf", "20", "-preset", "medium",
       "-af", "loudnorm=I=-16:LRA=11:TP=-1.5", "-ar", "48000", "-c:a", "aac", "-b:a", "192k", "-shortest",
       "-movflags", "+faststart", str(out)]
print("running:", " ".join(cmd[:6]), "...")
subprocess.run(cmd, check=True)
print("wrote", out, round(os.path.getsize(out) / 1e6, 1), "MB")

"""Assemble THE GLASS rough cut v001: all 102 shot positions, 13:00, with audio.

Video sources per shot, in order of preference:
  2D  : <r2d>/SH-xxx_2D_v001.mp4                      (tg2d engine, 1280x720)
  2D/3D SH-028–031 : the approved prototype v001      (27.0 s at 03:30)
  3D  : <c3d>/SH-xxx/frames/*.png                     (Blender EEVEE previews; --step 2 frames are doubled)
  else: a labelled placeholder slate (animatic slate + "PLACEHOLDER" band). Gaps are never stretched.

Audio: <roughcut_audio.wav> from 07_AUDIO/build_roughcut_audio.py (TEMP VO + beds + SFX).

Outputs (in --out):
  shots/SH-xxx.mp4 (normalised 1280x720 / 24 fps / exact length), roughcut_manifest.csv,
  THE_GLASS_roughcut_v001_720p_master.mp4 and THE_GLASS_roughcut_v001_1080p.mp4

Usage: python build_roughcut_v001.py --r2d D --c3d D --slates D --audio WAV --out D
"""
import argparse
import csv
import glob
import os
import pathlib
import shutil
import subprocess
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
FPS = 24
ap = argparse.ArgumentParser()
ap.add_argument("--r2d", required=True)
ap.add_argument("--c3d", required=True)
ap.add_argument("--slates", required=True)
ap.add_argument("--audio", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--ffmpeg", default=shutil.which("ffmpeg") or "ffmpeg")
a = ap.parse_args()
FF = a.ffmpeg
OUT = pathlib.Path(a.out)
(OUT / "shots").mkdir(parents=True, exist_ok=True)
PROTO = ROOT / "09_DELIVERABLES/tests/THE_GLASS_prototype_v001_0330-0357.mp4"
FONT = ROOT / "03_2D_ASSETS/typography/oswald-latin-500-normal.woff"
GRADE3D = "vignette=angle=PI/5,noise=alls=5:allf=t"


def tc(s):
    h, m, x = (int(v) for v in s.split(":"))
    return h * 3600 + m * 60 + x


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(" ".join(map(str, cmd))[:300] + "\n" + r.stderr[-800:])


def norm(vf_in, src_args, dst, n):
    run([FF, "-y", "-loglevel", "error", *src_args, "-vf",
         f"{vf_in}scale=1280:720:flags=lanczos,fps={FPS},format=yuv420p,setsar=1,tpad=stop_mode=clone:stop=-1",
         "-frames:v", str(n), "-an", "-c:v", "libx264", "-crf", "23", "-preset", "medium", str(dst)])


rows = list(csv.DictReader(open(ROOT / "00_PROJECT_MANAGEMENT/shot_tracker.csv", encoding="utf-8")))
manifest = []
proto_done = False
for r in rows:
    sid, typ = r["shot_id"], r["type"]
    n = int(round(float(r["duration_s"]) * FPS))
    dst = OUT / "shots" / f"{sid}.mp4"
    if sid in ("SH-028", "SH-029", "SH-030", "SH-031"):
        if not proto_done:
            norm("", ["-i", str(PROTO)], OUT / "shots" / "SH-028-031_prototype.mp4", 27 * FPS)
            proto_done = True
        manifest.append((sid, typ, "PROTOTYPE v001 (2D+3D)", str(OUT / "shots" / "SH-028-031_prototype.mp4"), n, sid == "SH-028"))
        continue
    src2d = os.path.join(a.r2d, f"{sid}_2D_v001.mp4")
    frames = sorted(glob.glob(os.path.join(a.c3d, sid, "frames", f"{sid}_*.png")))
    if typ == "2D" and os.path.exists(src2d):
        norm("", ["-i", src2d], dst, n)
        manifest.append((sid, typ, "2D tg2d v001", str(dst), n, True))
    elif typ == "3D" and frames:
        # frames may be every 2nd frame (Blender frame_step 2): hold each frame for the gap to the next one
        step = 1
        if len(frames) > 1:
            f0 = int(frames[0].rsplit("_", 1)[1][:4]); f1 = int(frames[1].rsplit("_", 1)[1][:4])
            step = max(1, f1 - f0)
        with tempfile.TemporaryDirectory() as td:
            lst = os.path.join(td, "list.txt")
            with open(lst, "w") as fh:
                for f in frames:
                    fh.write(f"file '{f}'\nduration {step / FPS:.6f}\n")
                fh.write(f"file '{frames[-1]}'\n")
            norm(f"{GRADE3D},", ["-f", "concat", "-safe", "0", "-i", lst], dst, n)
        manifest.append((sid, typ, f"3D Blender EEVEE preview (step {step}, {len(frames)} rendered frames)", str(dst), n, True))
    else:
        slate = os.path.join(a.slates, f"{sid}.png")
        band = (f"drawbox=x=0:y=ih-90:w=iw:h=90:color=0xA95149@0.9:t=fill,"
                f"drawtext=fontfile={FONT}:text='PLACEHOLDER – {sid} not yet animated':x=(w-tw)/2:y=h-68:fontsize=34:fontcolor=white,")
        norm(band, ["-loop", "1", "-framerate", str(FPS), "-i", slate], dst, n)
        manifest.append((sid, typ, "PLACEHOLDER slate", str(dst), n, True))
    print(sid, manifest[-1][2], flush=True)

# concat in order (the prototype file once, covering SH-028..031)
with open(OUT / "concat.txt", "w") as fh:
    for sid, typ, kind, path, n, include in manifest:
        if include:
            fh.write(f"file '{path}'\n")
master = OUT / "THE_GLASS_roughcut_v001_720p_master.mp4"
run([FF, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(OUT / "concat.txt"), "-i", a.audio,
     "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-af", "loudnorm=I=-16:LRA=11:TP=-1.5", "-ar", "48000", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(master)])
final = OUT / "THE_GLASS_roughcut_v001_1080p.mp4"
run([FF, "-y", "-loglevel", "error", "-i", str(master), "-vf", "scale=1920:1080:flags=lanczos,format=yuv420p",
     "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-c:a", "copy", "-movflags", "+faststart", str(final)])
with open(OUT / "roughcut_manifest.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["shot_id", "type", "source_kind", "clip", "frames"])
    for sid, typ, kind, path, n, inc in manifest:
        w.writerow([sid, typ, kind, os.path.relpath(path, OUT), n])
print("wrote", final)

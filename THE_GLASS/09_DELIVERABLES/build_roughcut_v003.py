"""Rough cut v003: all four 3D sequences from approved Higgsfield scenes + the ElevenLabs narration (Verdict).

Based on v002.

For each 3D sequence, if 06_AI_VIDEO/approved/<first shot>.mp4 exists (a 30 s clip covering the whole
sequence), it replaces that sequence's shot clips. Everything else is reused from roughcut_v001/shots.
Timing is unchanged (same 18,720 frames). Audio: 07_AUDIO/final_mix/v002/THE_GLASS_mix_v002_VERDICT.flac.

  python3 09_DELIVERABLES/build_roughcut_v003.py            # writes roughcut_v003/THE_GLASS_roughcut_v003_1080p.mp4
"""
import csv
import os
import pathlib
import shutil
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]
V1 = ROOT / "09_DELIVERABLES/roughcut_v001"
OUT = ROOT / "09_DELIVERABLES/roughcut_v003"
AUDIO = ROOT / "07_AUDIO/final_mix/v002/THE_GLASS_mix_v002_VERDICT.flac"
APPROVED = ROOT / "06_AI_VIDEO/approved"
FF = shutil.which("ffmpeg") or "ffmpeg"
SEQUENCES = {"SH-031": ["SH-031", "SH-032", "SH-033", "SH-034"], "SH-050": ["SH-050", "SH-051", "SH-052"],
             "SH-064": ["SH-064", "SH-065", "SH-066", "SH-067"], "SH-083": ["SH-083", "SH-084", "SH-085", "SH-086"]}
NORM = "fps=24,scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,setsar=1,format=yuv420p"


def run(cmd):
    subprocess.run(cmd, check=True)


def frames(p):
    out = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                          "stream=nb_read_frames", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout
    return int(out.strip() or 0)


OUT.mkdir(exist_ok=True)
(OUT / "shots").mkdir(exist_ok=True)
rows = list(csv.DictReader(open(V1 / "roughcut_manifest.csv", encoding="utf-8")))
fr = {r["shot_id"]: int(r["frames"]) for r in rows}
replaced = {}
for first, shots in SEQUENCES.items():
    src = APPROVED / f"{first}.mp4"
    if src.exists():
        n = sum(fr[s] for s in shots)
        dst = OUT / "shots" / f"{first}_HIGGSFIELD_seq.mp4"
        run([FF, "-y", "-v", "error", "-i", str(src), "-an", "-vf", f"{NORM},tpad=stop_mode=clone:stop_duration=2",
             "-frames:v", str(n), "-c:v", "libx264", "-crf", "18", "-preset", "medium", str(dst)])
        for s in shots:
            replaced[s] = (first, dst)
print("replaced sequences:", sorted({v[0] for v in replaced.values()}) or "none")

seq, done, manifest = [], set(), []
for r in rows:
    sid, clip = r["shot_id"], r["clip"]
    if sid in replaced:
        first, dst = replaced[sid]
        if first not in done:
            done.add(first)
            seq.append(dst)
        manifest.append({**r, "source_kind": "HIGGSFIELD Seedance 2.0 draft 480p (upscaled)", "clip": "shots/" + dst.name})
        continue
    if clip.endswith("SH-028-031_prototype.mp4") and "SH-031" in replaced:
        # prototype covers SH-028..031; keep only SH-028..030 (first 480 frames)
        if "proto" not in done:
            done.add("proto")
            dst = OUT / "shots" / "SH-028-030_prototype_trim.mp4"
            keep = fr["SH-028"] + fr["SH-029"] + fr["SH-030"]
            run([FF, "-y", "-v", "error", "-i", str(V1 / clip), "-an", "-frames:v", str(keep), "-c:v", "libx264",
                 "-crf", "18", "-preset", "medium", str(dst)])
            seq.append(dst)
        manifest.append({**r, "clip": "shots/SH-028-030_prototype_trim.mp4"})
        continue
    src = V1 / clip
    if src not in seq:
        seq.append(src)
    manifest.append(r)

total = sum(frames(p) for p in seq)
print("clips:", len(seq), "frames:", total, "(expect 18720)")
with open(OUT / "roughcut_manifest_v003.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(manifest)
lst = OUT / "concat_v003.txt"
lst.write_text("".join(f"file '{p.resolve().as_posix()}'\n" for p in seq), encoding="utf-8")
out = OUT / "THE_GLASS_roughcut_v003_1080p.mp4"
run([FF, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-i", str(AUDIO),
     "-map", "0:v", "-map", "1:a", "-vf", "scale=1920:1080:flags=lanczos,format=yuv420p", "-c:v", "libx264", "-crf", "20",
     "-preset", os.environ.get("THE_GLASS_PRESET", "veryfast"), "-af", "loudnorm=I=-16:LRA=11:TP=-1.5", "-ar", "48000",
     "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out)])
print("wrote", out, round(out.stat().st_size / 1e6, 1), "MB")

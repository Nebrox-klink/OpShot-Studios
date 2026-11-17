"""DaVinci Resolve: create the THE GLASS master project, bins, timeline, shot markers
and placeholders from 00_PROJECT_MANAGEMENT/shot_tracker.csv.

STATUS: UNTESTED. It was written in a cloud container that has no Resolve installed.
It uses only the documented Resolve scripting API (Resolve 18+). Run it on the
Lenovo laptop with Resolve OPEN:

  Windows (PowerShell), Resolve Studio or free 18.5+ with "External scripting: Local":
    $env:RESOLVE_SCRIPT_API = "C:\\ProgramData\\Blackmagic Design\\DaVinci Resolve\\Support\\Developer\\Scripting"
    $env:RESOLVE_SCRIPT_LIB = "C:\\Program Files\\Blackmagic Design\\DaVinci Resolve\\fusionscript.dll"
    $env:PYTHONPATH = "$env:PYTHONPATH;$env:RESOLVE_SCRIPT_API\\Modules\\"
    python resolve_build_master_timeline.py --root "D:\\THE_GLASS"

  Or copy it to %APPDATA%\\Blackmagic Design\\DaVinci Resolve\\Support\\Fusion\\Scripts\\Utility
  and run it from Workspace > Scripts (edit ROOT below first).

Behaviour:
  * Creates (or opens) the project "THE GLASS — NOKAS DOCUMENTARY": 1920x1080, 24 fps, 48 kHz audio.
  * Creates bins: Voiceover, 2D footage, Blender renders, AI-enhanced, SFX, Music, Graphics, Reference, Animatic.
  * Imports the prototype and the animatic if they exist.
  * Creates the timeline THE_GLASS_master_v001 with V1–V4 and A1–A4, and adds a marker for each of the
    102 shots (blue = 2D, red = 3D) with the VO line, the source class and the status as the marker note.
  * Places the animatic on V1 as a full-length guide, and the prototype at 00:03:30 on V2.
It never deletes anything. If the project or timeline already exists, it opens it and only adds markers
that are missing.
"""
import argparse
import csv
import os
import sys

ap = argparse.ArgumentParser()
ap.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
args = ap.parse_args()
ROOT = args.root

try:
    import DaVinciResolveScript as dvr  # noqa: N813
except ImportError:
    sys.exit("DaVinciResolveScript not found: set RESOLVE_SCRIPT_API / PYTHONPATH (see header).")

FPS = 24
PROJECT = "THE GLASS — NOKAS DOCUMENTARY"
TIMELINE = "THE_GLASS_master_v001"
BINS = ["Voiceover", "2D footage", "Blender renders", "AI-enhanced", "SFX", "Music", "Graphics", "Reference", "Animatic"]


def tc2f(tc):
    h, m, s = (int(x) for x in tc.split(":"))
    return (h * 3600 + m * 60 + s) * FPS


resolve = dvr.scriptapp("Resolve")
if resolve is None:
    sys.exit("Resolve is not running, or external scripting is disabled (Preferences > System > General).")
pm = resolve.GetProjectManager()
project = pm.LoadProject(PROJECT) or pm.CreateProject(PROJECT)
if not project:
    sys.exit("Could not create or load the project.")
for k, v in (("timelineResolutionWidth", "1920"), ("timelineResolutionHeight", "1080"),
             ("timelineFrameRate", "24"), ("timelinePlaybackFrameRate", "24"), ("audioSampleRate", "48000")):
    ok = project.SetSetting(k, v)
    print(f"setting {k}={v}: {'ok' if ok else 'NOT applied (may be locked once media exists)'}")

mp = project.GetMediaPool()
root = mp.GetRootFolder()
existing = {f.GetName(): f for f in root.GetSubFolderList()}
bins = {name: existing.get(name) or mp.AddSubFolder(root, name) for name in BINS}


def import_into(bin_name, path):
    if not os.path.exists(path):
        print("missing (skipped):", path)
        return None
    mp.SetCurrentFolder(bins[bin_name])
    items = mp.ImportMedia([path])
    print("imported:", path, "->", bin_name, "OK" if items else "FAILED")
    return items[0] if items else None


animatic = import_into("Animatic", os.path.join(ROOT, "01_SCRIPT_STORYBOARD/animatic/THE_GLASS_animatic_v001.mp4"))
proto = import_into("2D footage", os.path.join(ROOT, "09_DELIVERABLES/tests/THE_GLASS_prototype_v001_0330-0357.mp4"))

timeline = None
for i in range(1, project.GetTimelineCount() + 1):
    t = project.GetTimelineByIndex(i)
    if t.GetName() == TIMELINE:
        timeline = t
if timeline is None:
    mp.SetCurrentFolder(root)
    timeline = mp.CreateEmptyTimeline(TIMELINE)
    for _ in range(3):
        timeline.AddTrack("video")
    for _ in range(3):
        timeline.AddTrack("audio", "stereo")
    names = {("video", 1): "V1 2D main", ("video", 2): "V2 3D / AI", ("video", 3): "V3 overlays/maps",
             ("video", 4): "V4 titles/glass FX", ("audio", 1): "A1 narration", ("audio", 2): "A2 atmos",
             ("audio", 3): "A3 SFX", ("audio", 4): "A4 music"}
    for (kind, idx), nm in names.items():
        timeline.SetTrackName(kind, idx, nm)
project.SetCurrentTimeline(timeline)
start = timeline.GetStartFrame()  # usually 01:00:00:00 = 86400

if animatic:
    mp.AppendToTimeline([{"mediaPoolItem": animatic, "trackIndex": 1, "recordFrame": start}])
if proto:
    mp.AppendToTimeline([{"mediaPoolItem": proto, "trackIndex": 2, "recordFrame": start + tc2f("00:03:30")}])

have = set((timeline.GetMarkers() or {}).keys())
rows = list(csv.DictReader(open(os.path.join(ROOT, "00_PROJECT_MANAGEMENT/shot_tracker.csv"), encoding="utf-8")))
added = 0
for r in rows:
    f = tc2f(r["start"])  # marker frames are relative to the timeline start
    if f in have:
        continue
    dur = max(1, int(float(r["duration_s"]) * FPS))
    note = f"{r['vo_exact']} | {r['source_class']} ({r['source_ids']}) | {r['production_status']}"
    if timeline.AddMarker(f, "Red" if r["type"] == "3D" else "Blue", r["shot_id"], note[:1000], dur):
        added += 1
print(f"markers added: {added} / {len(rows)}")
pm.SaveProject()
print("saved project:", PROJECT)

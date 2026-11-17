"""DaVinci Resolve: build the THE GLASS master project from the rough-cut shot clips (v002).

Works two ways:
  1) Inside Resolve: copy this file to
     %APPDATA%\\Blackmagic Design\\DaVinci Resolve\\Support\\Fusion\\Scripts\\Utility\\
     and run Workspace > Scripts > Utility > resolve_build_master_timeline_v002
  2) Outside Resolve (needs Preferences > System > General > "External scripting using: Local"):
     py -3.12 08_DAVINCI_RESOLVE\\resolve_build_master_timeline_v002.py

It never deletes anything. It creates or opens the project "THE GLASS — NOKAS DOCUMENTARY"
(1920x1080, 24 fps, 48 kHz), imports 09_DELIVERABLES/roughcut_v001/shots/*.mp4 into bins
(2D / 3D / Prototype / Placeholders), and builds the timeline THE_GLASS_roughcut_v001:
V1 = every shot in order at its exact timecode, A1 = the TEMP narration mix, plus 102 markers
(blue = 2D, red = 3D, yellow = placeholder) carrying the VO line and the source class.
It writes a log next to itself.
"""
import csv
import os
import sys
import time

THIS = os.path.abspath(__file__) if "__file__" in globals() else ""
ROOT = os.environ.get("THE_GLASS_ROOT") or (os.path.dirname(os.path.dirname(THIS)) if THIS else os.path.expanduser(r"~\Documents\THE_GLASS_repo\THE_GLASS"))
RC = os.path.join(ROOT, "09_DELIVERABLES", "roughcut_v001")
LOG = os.path.join(ROOT, "08_DAVINCI_RESOLVE", "resolve_build_v002.log")
PROJECT = "THE GLASS — NOKAS DOCUMENTARY"
TIMELINE = "THE_GLASS_roughcut_v001"
FPS = 24
lines = []


def log(*a):
    s = " ".join(str(x) for x in a)
    lines.append(s)
    print(s, flush=True)
    try:
        open(LOG, "w", encoding="utf-8").write("\n".join(lines))
    except Exception:
        pass


def get_resolve():
    g = globals()
    if g.get("resolve"):
        return g["resolve"]
    for getter in (lambda: bmd.scriptapp("Resolve"), lambda: app.GetResolve()):  # noqa: F821 (inside Resolve)
        try:
            r = getter()
            if r:
                return r
        except Exception:
            pass
    api = os.environ.get("RESOLVE_SCRIPT_API", r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting")
    os.environ.setdefault("RESOLVE_SCRIPT_LIB", r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll")
    sys.path.append(os.path.join(api, "Modules"))
    import DaVinciResolveScript as dvr
    return dvr.scriptapp("Resolve")


def tc2f(tc):
    h, m, s = (int(x) for x in tc.split(":"))
    return (h * 3600 + m * 60 + s) * FPS


resolve = get_resolve()
if not resolve:
    log("ERROR: cannot reach Resolve. Enable Preferences > System > General > External scripting using: Local, or run from Workspace > Scripts.")
    sys.exit(2)
log("Resolve", resolve.GetVersionString(), "| root", ROOT)
pm = resolve.GetProjectManager()
proj = pm.LoadProject(PROJECT) or pm.CreateProject(PROJECT)
for k, v in (("timelineResolutionWidth", "1920"), ("timelineResolutionHeight", "1080"), ("timelineFrameRate", "24"),
             ("timelinePlaybackFrameRate", "24"), ("audioSampleRate", "48000")):
    log("setting", k, v, proj.SetSetting(k, v))
mp = proj.GetMediaPool()
root = mp.GetRootFolder()
have = {f.GetName(): f for f in root.GetSubFolderList()}
bins = {n: have.get(n) or mp.AddSubFolder(root, n) for n in ("2D animation", "3D Blender previews", "Prototype", "Placeholders", "Audio TEMP")}

manifest = list(csv.DictReader(open(os.path.join(RC, "roughcut_manifest.csv"), encoding="utf-8")))
tracker = {r["shot_id"]: r for r in csv.DictReader(open(os.path.join(ROOT, "00_PROJECT_MANAGEMENT", "shot_tracker.csv"), encoding="utf-8"))}
items = {}
for r in manifest:
    clip = os.path.join(RC, r["clip"])
    if clip in items:
        continue
    kind = r["source_kind"]
    b = "Prototype" if kind.startswith("PROTOTYPE") else "Placeholders" if kind.startswith("PLACEHOLDER") else "3D Blender previews" if r["type"] == "3D" else "2D animation"
    mp.SetCurrentFolder(bins[b])
    got = mp.ImportMedia([clip])
    items[clip] = got[0] if got else None
log("imported clips:", sum(1 for v in items.values() if v), "/", len(items))
mp.SetCurrentFolder(bins["Audio TEMP"])
aud = mp.ImportMedia([os.path.join(RC, "THE_GLASS_roughcut_v001_mix_TEMP.flac")])
log("imported audio:", bool(aud))

mp.SetCurrentFolder(root)
existing = [proj.GetTimelineByIndex(i + 1) for i in range(proj.GetTimelineCount())]
name = TIMELINE if TIMELINE not in [t.GetName() for t in existing] else TIMELINE + "_" + time.strftime("%H%M")
tl = mp.CreateEmptyTimeline(name)
proj.SetCurrentTimeline(tl)
start = tl.GetStartFrame()
placed = 0
done = set()
for r in manifest:
    clip = os.path.join(RC, r["clip"])
    if clip in done or not items.get(clip):
        continue
    done.add(clip)
    rec = start + tc2f(tracker[r["shot_id"]]["start"])
    ok = mp.AppendToTimeline([{"mediaPoolItem": items[clip], "trackIndex": 1, "recordFrame": rec}])
    placed += 1 if ok else 0
log("placed on V1:", placed, "/", len(done))
if aud:
    ok = mp.AppendToTimeline([{"mediaPoolItem": aud[0], "trackIndex": 1, "mediaType": 2, "recordFrame": start}])
    log("audio on A1:", bool(ok))
marks = 0
kinds = {r["shot_id"]: r["source_kind"] for r in manifest}
for sid, r in tracker.items():
    col = "Yellow" if kinds.get(sid, "").startswith("PLACEHOLDER") else ("Red" if r["type"] == "3D" else "Blue")
    note = f"{r['vo_exact']} | {r['source_class']} ({r['source_ids']}) | {kinds.get(sid, '')}"
    if tl.AddMarker(tc2f(r["start"]), col, sid, note[:1000], max(1, int(float(r["duration_s"]) * FPS))):
        marks += 1
log("markers:", marks, "/", len(tracker))
log("timeline frames:", tl.GetEndFrame() - tl.GetStartFrame(), "(expect", 13 * 60 * FPS, ")")
log("saved:", pm.SaveProject())

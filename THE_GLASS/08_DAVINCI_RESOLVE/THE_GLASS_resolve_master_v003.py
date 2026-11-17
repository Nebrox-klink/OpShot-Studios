"""THE GLASS: DaVinci Resolve master timeline + high-quality render job (v003, standalone).

HOW TO USE (Resolve free or Studio, Windows):
  1. Copy this file to
       %APPDATA%\\Blackmagic Design\\DaVinci Resolve\\Support\\Fusion\\Scripts\\Utility\\
  2. Restart Resolve, then run  Workspace > Scripts > Utility > THE_GLASS_resolve_master_v003
  3. Read the log it writes: THE_GLASS\\08_DAVINCI_RESOLVE\\resolve_master_v003.log

WHAT IT DOES (it never deletes or overwrites anything):
  - Creates or opens the project "THE GLASS — NOKAS DOCUMENTARY" (1920x1080, 24 fps, 48 kHz).
  - Imports the 102 rough-cut shot clips into bins and the TEMP audio mix.
  - Builds a new timeline (a new name if one already exists):
      V1 = rough cut, every shot at its exact timecode
      V2 = your Higgsfield clips (see below), trimmed to each shot's length, on top of V1
      A1 = TEMP narration/sound mix
      markers on every shot (blue 2D, red 3D, green = Higgsfield replacement)
  - Sets high-quality render settings and adds ONE render job to the queue.
    It does NOT start the render unless START_RENDER = True below.

HIGGSFIELD CLIPS:
  Put your exported Higgsfield videos in  THE_GLASS\\06_AI_VIDEO\\approved\\
  and name each one after the shot it replaces, e.g.  SH-064.mp4  or  SH-064_take2.mp4
  (the first file whose name starts with the shot ID is used). Any shot without a clip keeps
  the rough-cut version on V1, so the film always plays end to end. If a clip is shorter than
  the shot, the rough cut shows through for the rest of the shot.
"""
import csv
import glob
import os
import sys
import time

# ---------------- settings you may change ----------------
ROOT = os.path.join(os.path.expanduser("~"), "Documents", "THE_GLASS_repo", "THE_GLASS")
HIGGSFIELD_DIR = os.path.join(ROOT, "06_AI_VIDEO", "approved")
RENDER_DIR = os.path.join(ROOT, "09_DELIVERABLES", "resolve_renders")
RENDER_NAME = "THE_GLASS_roughcut_v002_1080p"
RENDER_FORMAT, RENDER_CODEC = "mp4", "H264"   # Studio users can use "mov", "ProRes422HQ"
VIDEO_QUALITY = "Best"                       # "Least" / "Low" / "Medium" / "High" / "Best"
START_RENDER = False                          # True = start rendering straight away
# ----------------------------------------------------------

ROOT = os.environ.get("THE_GLASS_ROOT", ROOT)
RC = os.path.join(ROOT, "09_DELIVERABLES", "roughcut_v001")
LOG = os.path.join(ROOT, "08_DAVINCI_RESOLVE", "resolve_master_v003.log")
PROJECT = "THE GLASS — NOKAS DOCUMENTARY"
TIMELINE = "THE_GLASS_master_v003"
FPS = 24
lines = []


def log(*a):
    s = " ".join(str(x) for x in a)
    lines.append(s)
    print(s, flush=True)
    try:
        with open(LOG, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines))
    except Exception:
        pass


def get_resolve():
    g = globals()
    if g.get("resolve"):
        return g["resolve"]
    for getter in (lambda: bmd.scriptapp("Resolve"), lambda: app.GetResolve()):  # noqa: F821 (defined inside Resolve)
        try:
            r = getter()
            if r:
                return r
        except Exception:
            pass
    try:
        api = os.environ.get("RESOLVE_SCRIPT_API", r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting")
        os.environ.setdefault("RESOLVE_SCRIPT_LIB", r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll")
        sys.path.append(os.path.join(api, "Modules"))
        import DaVinciResolveScript as dvr
        return dvr.scriptapp("Resolve")
    except Exception:
        return None


def tc2f(tc):
    h, m, s = (int(x) for x in tc.split(":"))
    return (h * 3600 + m * 60 + s) * FPS


def main():
    resolve = get_resolve()
    if not resolve:
        log("ERROR: cannot reach Resolve. Run this from Workspace > Scripts > Utility inside Resolve.")
        return
    if not os.path.isdir(RC):
        log("ERROR: rough-cut folder not found:", RC, "| set ROOT at the top of this script.")
        return
    log("Resolve", resolve.GetVersionString(), "| root", ROOT)

    pm = resolve.GetProjectManager()
    proj = pm.LoadProject(PROJECT) or pm.CreateProject(PROJECT)
    if not proj:
        log("ERROR: could not open or create the project. Close any open project and try again.")
        return
    for k, v in (("timelineResolutionWidth", "1920"), ("timelineResolutionHeight", "1080"),
                 ("timelineFrameRate", "24"), ("timelinePlaybackFrameRate", "24"), ("audioSampleRate", "48000")):
        log("setting", k, v, proj.SetSetting(k, v))

    mp = proj.GetMediaPool()
    root = mp.GetRootFolder()
    have = {f.GetName(): f for f in root.GetSubFolderList()}
    bins = {n: have.get(n) or mp.AddSubFolder(root, n) for n in
            ("2D animation", "3D Blender previews", "Prototype", "Higgsfield", "Audio TEMP")}

    manifest = list(csv.DictReader(open(os.path.join(RC, "roughcut_manifest.csv"), encoding="utf-8")))
    tracker = {r["shot_id"]: r for r in csv.DictReader(
        open(os.path.join(ROOT, "00_PROJECT_MANAGEMENT", "shot_tracker.csv"), encoding="utf-8"))}

    # rough-cut clips (some clips cover several shot IDs, e.g. the prototype)
    items = {}
    for r in manifest:
        clip = os.path.join(RC, r["clip"])
        if clip in items or not os.path.isfile(clip):
            continue
        kind = r["source_kind"]
        b = "Prototype" if kind.startswith("PROTOTYPE") else "3D Blender previews" if r["type"] == "3D" else "2D animation"
        mp.SetCurrentFolder(bins[b])
        got = mp.ImportMedia([clip])
        items[clip] = got[0] if got else None
    log("imported rough-cut clips:", sum(1 for v in items.values() if v), "/", len(items))

    # Higgsfield replacements, matched by shot ID prefix
    hf = {}
    if os.path.isdir(HIGGSFIELD_DIR):
        mp.SetCurrentFolder(bins["Higgsfield"])
        for sid in tracker:
            files = sorted(f for ext in ("mp4", "mov", "webm", "mkv")
                           for f in glob.glob(os.path.join(HIGGSFIELD_DIR, f"{sid}*.{ext}")))
            if files:
                got = mp.ImportMedia([files[0]])
                if got:
                    hf[sid] = (got[0], os.path.basename(files[0]))
    log("Higgsfield clips found:", len(hf), sorted(hf) or "(none yet; folder " + HIGGSFIELD_DIR + ")")

    mp.SetCurrentFolder(bins["Audio TEMP"])
    aud = mp.ImportMedia([os.path.join(RC, "THE_GLASS_roughcut_v001_mix_TEMP.flac")])
    log("imported audio:", bool(aud))

    # timeline
    mp.SetCurrentFolder(root)
    names = [proj.GetTimelineByIndex(i + 1).GetName() for i in range(proj.GetTimelineCount())]
    name = TIMELINE if TIMELINE not in names else TIMELINE + "_" + time.strftime("%Y%m%d_%H%M")
    tl = mp.CreateEmptyTimeline(name)
    proj.SetCurrentTimeline(tl)
    start = tl.GetStartFrame()

    placed, done = 0, set()
    for r in manifest:
        clip = os.path.join(RC, r["clip"])
        if clip in done or not items.get(clip):
            continue
        done.add(clip)
        rec = start + tc2f(tracker[r["shot_id"]]["start"])
        if mp.AppendToTimeline([{"mediaPoolItem": items[clip], "trackIndex": 1, "recordFrame": rec}]):
            placed += 1
    log("V1 rough cut placed:", placed, "/", len(done))

    if hf:
        while tl.GetTrackCount("video") < 2:
            if not tl.AddTrack("video"):
                break
        hf_placed = 0
        for sid, (item, fname) in sorted(hf.items()):
            t = tracker[sid]
            dur = max(1, int(float(t["duration_s"]) * FPS))
            ok = mp.AppendToTimeline([{"mediaPoolItem": item, "trackIndex": 2, "mediaType": 1,
                                       "startFrame": 0, "endFrame": dur - 1,
                                       "recordFrame": start + tc2f(t["start"])}])
            log("  V2", sid, fname, "OK" if ok else "FAILED")
            hf_placed += 1 if ok else 0
        log("V2 Higgsfield placed:", hf_placed, "/", len(hf))

    if aud:
        ok = mp.AppendToTimeline([{"mediaPoolItem": aud[0], "trackIndex": 1, "mediaType": 2, "recordFrame": start}])
        log("A1 audio:", bool(ok))

    marks = 0
    for sid, r in tracker.items():
        col = "Green" if sid in hf else ("Red" if r["type"] == "3D" else "Blue")
        note = f"{r['vo_exact']} | {r['source_class']} ({r['source_ids']})"
        if sid in hf:
            note = "HIGGSFIELD: " + hf[sid][1] + " | " + note
        if tl.AddMarker(tc2f(r["start"]), col, sid, note[:1000], max(1, int(float(r["duration_s"]) * FPS))):
            marks += 1
    log("markers:", marks, "/", len(tracker))
    log("timeline frames:", tl.GetEndFrame() - tl.GetStartFrame(), "(expect", 13 * 60 * FPS, ")")

    # render job
    os.makedirs(RENDER_DIR, exist_ok=True)
    log("render format:", RENDER_FORMAT, RENDER_CODEC, proj.SetCurrentRenderFormatAndCodec(RENDER_FORMAT, RENDER_CODEC))
    log("render settings:", proj.SetRenderSettings({
        "SelectAllFrames": True, "TargetDir": RENDER_DIR, "CustomName": RENDER_NAME,
        "ExportVideo": True, "ExportAudio": True, "FormatWidth": 1920, "FormatHeight": 1080,
        "FrameRate": 24.0, "VideoQuality": VIDEO_QUALITY, "AudioCodec": "aac",
        "AudioSampleRate": 48000, "AudioBitDepth": 24}))
    job = proj.AddRenderJob()
    log("render job added:", job or "FAILED", "->", os.path.join(RENDER_DIR, RENDER_NAME + "." + RENDER_FORMAT))
    if job and START_RENDER:
        log("render started:", proj.StartRendering(job))
    elif job:
        log("Render not started. Open the Deliver page and press Render All when ready.")
    log("saved:", pm.SaveProject())


main()

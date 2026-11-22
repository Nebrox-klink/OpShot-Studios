"""Shared film timeline: one place for the rules the mix, the picture edit and the subtitles must agree on.

Profiles (env TIMING):
  tight  (default, v009): tightened narration (pauses <= 0.8 s), 1 s lead-in + 0.5 s tail per scene (about 1.5 s
         between scenes), 3 s white silence at 08:17. Scenes 1, 13 and 24 keep their scripted slot and their
         original audio, because their sound design is timed to it (cold open, the 113 counter, the ending).
  v008b: the v008b/v008d rule (original audio, half of the leftover slot, 6 s silence).

timeline(root) -> dict with CARD, LEAD, SIL17, scenes {n: {start, length, chunks: [(id, offset_in_scene, path)]}},
                  and warp(scene, offset) mapping a cue offset written against the original audio to the new one.
"""
import json
import os
import re
import subprocess

PROFILE = os.environ.get("TIMING", "tight")
CARD, LEAD = 4.0, 1.0
FIXED = (1, 13, 24)


def _dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                capture_output=True, text=True, check=True).stdout)


def timeline(root):
    script = os.path.join(root, "01_SCRIPT_STORYBOARD/revised/THE_GLASS_script_v008.md")
    orig = os.path.join(root, "07_AUDIO/atlas_v008")
    tight = os.path.join(root, "07_AUDIO/atlas_v008_tight")
    sil17 = 3.0 if PROFILE == "tight" else 6.0
    maps = json.load(open(os.path.join(tight, "time_maps.json"))) if PROFILE == "tight" else {}
    scene_re = re.compile(r"^#### Scene (\d+) · (.+?) \((\d+):(\d+)–(\d+):(\d+)\)")
    slots = {}
    for line in open(script, encoding="utf-8"):
        if m := scene_re.match(line):
            n, _, a, b, c, d = m.groups()
            slots[int(n)] = (int(c) * 60 + int(d)) - (int(a) * 60 + int(b))

    def path(cid, n):
        if PROFILE == "tight" and n not in FIXED:
            return os.path.join(tight, cid + ".flac")
        return os.path.join(orig, cid + ".mp3")

    scenes, t = {}, CARD
    for n in sorted(slots):
        if os.path.isfile(os.path.join(orig, f"S{n:02d}.mp3")):
            p = path(f"S{n:02d}", n)
            chunks = [(f"S{n:02d}", LEAD, p)]
            used = LEAD + _dur(p)
        else:
            pa, pb = path(f"S{n:02d}a", n), path(f"S{n:02d}b", n)
            da = _dur(pa)
            chunks = [(f"S{n:02d}a", LEAD, pa), (f"S{n:02d}b", LEAD + da + sil17, pb)]
            used = LEAD + da + sil17 + _dur(pb)
        if n in FIXED:
            length = slots[n]
        elif PROFILE == "tight":
            length = used + 0.5
        else:
            length = max(used + 0.5, used + (slots[n] - used) * 0.5)
        scenes[n] = {"start": t, "length": length, "chunks": chunks, "used": used, "slot": slots[n]}
        t += length

    def warp(n, off):
        """Move a cue offset written against the original audio onto the same word in the tightened audio."""
        if PROFILE != "tight" or n in FIXED or off <= LEAD:
            return off
        cid = scenes[n]["chunks"][0][0]
        knots = maps.get(cid)
        if not knots:
            return off
        x = off - LEAD
        prev_o, prev_n = 0.0, 0.0
        for o, nn in knots:
            if x <= o:
                if o == prev_o:
                    return LEAD + nn
                return LEAD + prev_n + (x - prev_o) * (nn - prev_n) / (o - prev_o) if nn - prev_n > 0 else LEAD + nn
            prev_o, prev_n = o, nn
        return LEAD + prev_n + (x - prev_o)

    return {"CARD": CARD, "LEAD": LEAD, "SIL17": sil17, "scenes": scenes, "total": t, "warp": warp,
            "profile": PROFILE}

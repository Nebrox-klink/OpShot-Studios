"""Estimate narration timing per scene from a script .md and write a clean narration TSV.

Usage: python narration_timing.py SCRIPT.md OUT.tsv [chars_per_sec]
Narration lines start with '> '. Source tags in backticks are stripped.
*(beat)* = 1 s, *(hold)* = 3 s, *(white ...)* = 6 s.
"""
import re
import sys

src, out = sys.argv[1], sys.argv[2]
cps = float(sys.argv[3]) if len(sys.argv) > 3 else 14.0
scene_re = re.compile(r"^#### Scene (\d+) · (.+?) \((\d+):(\d+)–(\d+):(\d+)\)")
scenes, cur = [], None
for line in open(src, encoding="utf-8"):
    m = scene_re.match(line)
    if m:
        n, title, a, b, c, d = m.groups()
        cur = dict(n=int(n), title=title, dur=(int(c) * 60 + int(d)) - (int(a) * 60 + int(b)), lines=[], pause=0.0)
        scenes.append(cur)
        continue
    if cur is None or not line.startswith("> "):
        continue
    body = line[2:].strip()
    if body.startswith("*("):
        cur["pause"] += 6 if "white" in body else 3 if "hold" in body else 1
        continue
    tags = " ".join(re.findall(r"`([^`]*)`", body))
    text = re.sub(r"\s*`[^`]*`", "", body).strip()
    cur["lines"].append((text, tags))

rows, total_chars, total_est = [], 0, 0.0
with open(out, "w", encoding="utf-8") as fh:
    fh.write("scene\tline\ttext\tsource_tags\test_sec\n")
    for s in scenes:
        chars = 0
        for i, (t, tags) in enumerate(s["lines"], 1):
            fh.write(f"{s['n']}\t{i}\t{t}\t{tags}\t{len(t) / cps:.1f}\n")
            chars += len(t)
        est = chars / cps + s["pause"]
        total_chars += chars
        total_est += est
        flag = "OVER" if est > s["dur"] else ("ok" if est > 0.5 * s["dur"] else "airy")
        rows.append(f"| {s['n']} | {s['title']} | {s['dur']} s | {chars} | {est:.0f} s | {100 * est / s['dur']:.0f}% | {flag} |")
print("| Scene | Title | Slot | Characters | Read + pauses | Fill | Check |")
print("|---|---|---|---|---|---|---|")
print("\n".join(rows))
print(f"| **Total** | | **{sum(s['dur'] for s in scenes)} s** | **{total_chars}** | **{total_est:.0f} s** | **{100 * total_est / sum(s['dur'] for s in scenes):.0f}%** | |")

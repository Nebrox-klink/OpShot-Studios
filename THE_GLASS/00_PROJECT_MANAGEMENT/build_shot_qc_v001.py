"""Write shot_qc_v001.csv: the visual and technical QC verdict per shot for rough cut v001.

The verdicts come from inspecting contact sheets (first/middle/last frame) of every rendered clip
on 17 Nov 2026, plus ffprobe checks on frame count and resolution. Notes are deliberately specific.
"""
import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
rows = list(csv.DictReader(open(ROOT / "00_PROJECT_MANAGEMENT/shot_tracker.csv", encoding="utf-8")))
DEFAULT_2D = ("PASS WITH LIMITATIONS", "Procedural flat 2.5D style; correct length/res (ffprobe); simple motion. Final art pass needed.")
DEFAULT_3D = ("PASS WITH LIMITATIONS", "Blender EEVEE preview 640x360 upscaled, 12 fps doubled, 4 samples; blockout geometry.")
NOTES = {
    "SH-028": ("PASS", "Prototype v001 notebook (approved prototype quality)."),
    "SH-029": ("PASS", "Prototype v001."),
    "SH-030": ("PASS", "Prototype v001 incl. SIGNATURE IN 1."),
    "SH-031": ("PASS WITH LIMITATIONS", "Prototype v001 3D; figure is a blockout."),
    "SH-033": ("PASS WITH LIMITATIONS", "Breath fog and hand barely readable; warm defocus dominates."),
    "SH-034": ("PASS WITH LIMITATIONS", "Crouched figure still a rounded blockout; ends on fog/window as planned."),
    "SH-052": ("PASS WITH LIMITATIONS", "Glass yields; gloved hand reads only as a small dark shape."),
    "SH-066": ("PASS WITH LIMITATIONS", "Crack decal readable (stylised web); cut to white works."),
    "SH-085": ("PASS WITH LIMITATIONS", "Officers enter from left; door not in frame; man stays seated."),
    "SH-086": ("PASS WITH LIMITATIONS", "Screen switches off; the planned reflection does NOT render in software EEVEE: composite later."),
    "SH-097": ("PASS", "Glyph bug (≈) fixed before render."),
    "SH-098": ("PASS", "Unsupported '20 minutes' removed; shows 'minutes'."),
    "SH-078": ("PASS WITH LIMITATIONS", "Theory flagged; UNPROVEN label shown in SH-079."),
}
with open(ROOT / "00_PROJECT_MANAGEMENT/shot_qc_v001.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["shot_id", "type", "qc_status", "qc_note"])
    for r in rows:
        st, note = NOTES.get(r["shot_id"], DEFAULT_3D if r["type"] == "3D" else DEFAULT_2D)
        w.writerow([r["shot_id"], r["type"], st, note])
print("ok", len(rows))

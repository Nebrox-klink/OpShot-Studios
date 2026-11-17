"""Write shot_tracker_v002.csv: the v1.1 tracker plus the production state that the rough cut actually used.

States (from the brief): NOT STARTED · ASSETS READY · BLOCKED · ANIMATING · PREVIEW RENDERED · QC FAILED ·
APPROVED FOR ROUGH CUT · FINAL RENDERED. QC: PASS · PASS WITH LIMITATIONS · FAIL · NOT VERIFIED.
Nothing is marked FINAL RENDERED, because everything here is rough-cut quality.
"""
import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
man = {r["shot_id"]: r for r in csv.DictReader(open(ROOT / "09_DELIVERABLES/roughcut_v001/roughcut_manifest.csv", encoding="utf-8"))}
qc = {r["shot_id"]: r for r in csv.DictReader(open(ROOT / "00_PROJECT_MANAGEMENT/shot_qc_v001.csv", encoding="utf-8"))} \
    if (ROOT / "00_PROJECT_MANAGEMENT/shot_qc_v001.csv").exists() else {}
rows = list(csv.DictReader(open(ROOT / "00_PROJECT_MANAGEMENT/shot_tracker.csv", encoding="utf-8")))
fields = list(rows[0].keys()) + ["rough_cut_source", "rough_cut_clip", "qc_status", "qc_note"]
for r in rows:
    m = man.get(r["shot_id"], {})
    kind = m.get("source_kind", "")
    q = qc.get(r["shot_id"], {})
    if kind.startswith("PLACEHOLDER"):
        r["production_status"] = "NOT STARTED (placeholder in cut)"
    elif kind:
        r["production_status"] = "APPROVED FOR ROUGH CUT" if q.get("qc_status", "").startswith("PASS") else "PREVIEW RENDERED"
    r["render_stage"] = "roughcut_v001"
    r["rough_cut_source"] = kind
    r["rough_cut_clip"] = m.get("clip", "")
    r["qc_status"] = q.get("qc_status", "NOT VERIFIED")
    r["qc_note"] = q.get("qc_note", "")
with open(ROOT / "00_PROJECT_MANAGEMENT/shot_tracker_v002.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=fields)
    w.writeheader()
    w.writerows(rows)
print("wrote shot_tracker_v002.csv", len(rows))

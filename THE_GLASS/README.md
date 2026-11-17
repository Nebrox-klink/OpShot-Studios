# THE GLASS: The NOKAS Robbery (production workspace)

A 13-minute animated documentary for YouTube. Most of it is 2D animation, with four 30-second 3D cinematic sequences. There is one narrator, and the narration is in English.

## Start here

| What | Where |
|---|---|
| **Playable prototype (27 s, 03:30–03:57)** | `09_DELIVERABLES/tests/THE_GLASS_prototype_v001_0330-0357.mp4` (clean) · `09_DELIVERABLES/reviews/THE_GLASS_prototype_v001_REVIEW.mp4` (shot IDs, 2D/3D tags, TEMP subtitles) |
| **13:00 animatic** | `01_SCRIPT_STORYBOARD/animatic/THE_GLASS_animatic_v001.mp4` + `vo_timing_report.csv` |
| Current script | `01_SCRIPT_STORYBOARD/revised/THE_GLASS_script_v004.md` |
| Current storyboard | `01_SCRIPT_STORYBOARD/revised/THE_GLASS_102_shot_storyboard_v1.1.xlsx` (English; 9 sheets incl. CHANGE LOG) |
| Originals (read-only) | `01_SCRIPT_STORYBOARD/originals/` |
| Shot tracker / sources / costs | `00_PROJECT_MANAGEMENT/shot_tracker.csv`, `source_log.csv`, `cost_tracker.csv` |
| Plan, environment, QC, log | `00_PROJECT_MANAGEMENT/production_plan.md`, `environment_report.md`, `quality_control.md`, `progress_log.md` |
| Style guide | `02_VISUAL_DEVELOPMENT/style_guide/THE_GLASS_style_guide.md` |

## Rebuild everything (all scripts are deterministic)

```bash
python3 01_SCRIPT_STORYBOARD/shot_lists/build_storyboard_v1_1.py                       # storyboard v1.1 (EN) + shot_tracker.csv
blender -b -P 05_BLENDER/scripts/build_SH031_courtyard.py -- --out <dir> --render anim  # 3D SH-031 (or: python with `pip install bpy`)
python3 04_2D_ANIMATION/source_projects/SH-028-030_notebook.py --out <dir> --threed <SH-031_0001.png>
python3 07_AUDIO/build_prototype_audio.py --out <dir>                                    # needs festival + festvox-us-slt-hts
bash 09_DELIVERABLES/tests/build_prototype_v001.sh <2d_frames> <3d_frames> <mix.wav>
python3 01_SCRIPT_STORYBOARD/animatic/build_animatic.py --out <dir> --prototype <prototype.mp4>
python 08_DAVINCI_RESOLVE/resolve_build_master_timeline.py --root <THE_GLASS>             # on the laptop, Resolve open: UNTESTED
```

## Honesty notes
- Everything was produced in a **cloud container**. The Lenovo laptop (Blender, Resolve) was **not connected**.
- **TEMP VO** is an offline TTS voice used as a timing guide. It is not the narrator.
- **No AI video generation** has been run (spending limit $0).
- The fact-check used **search-result summaries**, because the full-text sites were blocked. Primary sources are still outstanding.

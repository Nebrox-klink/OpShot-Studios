# THE GLASS: production status (17 Nov 2026, evening)

**This is ROUGH CUT v001. It is not publication-ready.** The narration is a temporary TTS voice, and the 3D shots are low-sample, half-frame-rate previews with blockout figures.

## What exists and has been verified

| Deliverable | State | Evidence |
|---|---|---|
| Rough cut, 13:00, all **102 shot positions**, **0 placeholders** | **Rendered and verified**: 1920×1080, 18,720 frames = 780.0 s, audio −16.4 LUFS integrated; sample frames from every sequence checked by eye | `09_DELIVERABLES/roughcut_v001/` (`THE_GLASS_roughcut_v001_1080p.mp4` is built locally; the shot clips and `roughcut_manifest.csv` are in git) |
| 2D animation, **84 shots** (tg2d engine, layered 2.5D, procedural art) | Rendered, 1280×720, 24 fps. Every frame count and resolution checked | `04_2D_ANIMATION/engine/` |
| Prototype SH-028–031 (notebook → glass → 3D) | Rendered (prototype v001) | `09_DELIVERABLES/tests/` |
| 3D, **15 shots in 4 sequences**, Blender | **Preview rendered**: EEVEE 640×360, 4 samples, every 2nd frame (12 fps doubled), upscaled | `.blend` builders in `05_BLENDER/scripts/` |
| Audio, 13:00 | TEMP: Festival TTS narration, procedural ambience/SFX/pad/piano, loudness-normalised to −16 LUFS | `07_AUDIO/build_roughcut_audio.py`, `vo_drift_roughcut_v001.csv` |
| Málaga correction (Chicoti internet café, no seafront) | Implemented in the script v004, storyboard v1.1, 3D 4 and 2D SH-082/087 | `source_log.csv` S06–S10 |
| Per-shot QC | `00_PROJECT_MANAGEMENT/shot_qc_v001.csv` | 102 rows |
| Shot tracker with actual state | `00_PROJECT_MANAGEMENT/shot_tracker_v002.csv`: 102 × APPROVED FOR ROUGH CUT (QC: 5 PASS, 97 PASS WITH LIMITATIONS); none FINAL RENDERED | Generated from the manifest |


## Update, 17 Nov 2026 late evening: rough cut v002 (Higgsfield scenes)
**Rough cut v002 is rendered and verified:** `roughcut_v002/THE_GLASS_roughcut_v002_1080p.mp4`, 1920×1080, 18,720 frames = 780.0 s. It is still a ROUGH CUT, not publication-ready.

What changed from v001: the 3D preview sequences 1–3 were replaced by Higgsfield scenes made with the course workflow (Blender blockout → reference video → Nano Banana look image → Seedance 2.0 video):

| Scene | File | Notes |
|---|---|---|
| 3D 1 "Through the Glass" | `06_AI_VIDEO/approved/SH-031.mp4` | 0–15 s and 22–30 s from the blockout reference; the 15–22 s fog close-up was animated from a still |
| 3D 2 "113" | `06_AI_VIDEO/approved/SH-050.mp4` | 0–8 s from the reference; 8–30 s from photoreal stills (the reference produced flat graphic "stars") |
| 3D 3 "The Windshield" | `06_AI_VIDEO/approved/SH-064.mp4` | Hands and sleeve only, no head; the crack is fainter than planned |
| 3D 4 "One Year to the Day" | still the Blender preview | Not generated yet |

**Limits:**
- All Higgsfield clips are Seedance 2.0 *fast* 480p drafts, upscaled, with no generated audio.
- Final 1080p versions need a price check and the user's approval.

**Credits:** about 220 Higgsfield credits used for drafts, look images and stills; balance about 990.

**Resolve:** run `THE_GLASS_resolve_master_v003` from the Scripts menu. It puts the approved clips on V2 over the rough cut.

## Where the work ran (no blurring)
- **Cloud container:** all 2D, all 3D previews, the audio and the assembly.
- **Your laptop** (through the Higgsfield Blender bridge): the environment audit, starting/restarting DaVinci Resolve, the repo clone, and the local 1080p rebuild.

## DaVinci Resolve
- Resolve 21.2 **free** is installed and runs. You enabled External scripting (the preference file shows `System.Scripting.Mode = 1`), yet `scriptapp("Resolve")` still returns None after two restarts. The most likely reason is that external scripting is a Resolve **Studio** feature.
- Workaround (works in the free edition): the menu script `THE_GLASS_build_master_timeline_MENU` is installed in Resolve's Scripts folder. **Workspace → Scripts → Utility → THE_GLASS_build_master_timeline_MENU** imports every clip and the audio, places the 102 shots at their timecodes on V1 and the audio on A1, adds 102 markers, and saves the project "THE GLASS — NOKAS DOCUMENTARY". **This has not been run yet, so the Resolve project does not exist yet.**

## Known limitations (in order of impact)
1. **Narration is TEMP TTS.** 15 lines start more than 0.5 s late (at most 2.9 s), so they don't overlap. Record the real narrator, then re-time.
2. **3D quality:** 12 fps doubled to 24, 4 samples, blockout figures. SH-086's planned screen reflection does not render; the 2D SH-087 card carries the transition.
3. **2D style:** coherent but simple (flat silhouettes, procedural houses). There's no hand-drawn illustration pass yet.
4. **Facts still open:** 113 shots (secondary sources only), the arrest date (5 vs 6 April 2005), "third attempt", and "more than a year" of planning.
5. **Music** is a minimal synthesised pad and piano (licence-free).

## Higgsfield
Balance **10 credits** (Ultra). No generation was run: the spending limit is $0, and 10 credits are not enough for a meaningful video test. The prompts are ready in `06_AI_VIDEO/prompts/`.

## Recommended next steps
1. Run the Resolve menu script once. Then replace the TEMP narration with a real recording on A1 and re-time.
2. Re-render the 15 3D shots on the laptop GPU at 1080p, 24 fps (full frames) using the same scripts.
3. Make an illustration pass on the most visible 2D sets: Stavanger, the NOKAS façade, the counting room.
4. Resolve the four open fact flags against court material.

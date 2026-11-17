# THE GLASS: Production plan and phase status

Status words used here: **Planned → Created → Rendered → Visually checked → Approved**. Nothing in this project is *Approved* yet. Only you can approve.

## Phase status (17 Nov 2026)

| Phase | Status | Evidence |
|---|---|---|
| **A** Environment and setup | ✅ Done in the **cloud container**. ❌ The laptop was not reachable | `environment_report.md`, folder tree |
| **B** Script correction and scene mapping | ✅ Created | Script `v004`, storyboard `v1.1` (148 field changes, ENDRINGSLOGG sheet), `source_log.csv`, `shot_tracker.csv` |
| **C** Visual development | 🟡 Partly done | Style guide v0.1, palette, typography, transition board, 1 environment blockout. **Character designs are missing** |
| **D** First prototype (27 s) | ✅ Rendered and visually checked by me | `09_DELIVERABLES/tests/THE_GLASS_prototype_v001_0330-0357.mp4` |
| **E** Resolve assembly | 🟡 The animatic is rendered. The Resolve script is written but **untested** | `01_SCRIPT_STORYBOARD/animatic/…`, `08_DAVINCI_RESOLVE/resolve_build_master_timeline.py` |
| **F** Full production | ⬜ Not started | — |

## Decisions only you can make
1. **Laptop access.** Connect the `THE_GLASS` folder through Remote Control, or run the Blender and Resolve scripts yourself.
2. **Narrator voice.** Record yourself or a hired voice, or use ElevenLabs (the connector is available, but it **costs credits**). Right now only a robotic TEMP TTS exists.
3. **First paid AI test.** One 5 s test on SH-031 (prompt ready). The limit is $0 until you say otherwise.
4. **Source access.** The court rulings (Stavanger tingrett and Gulating lagmannsrett) or the newspaper archive are needed to lock 113 shots, the arrest date (5 or 6 April 2005), "third attempt" and the sentences.
5. **Character design direction for the silhouettes.** The prototype figure is a crude blockout.

## Next batches (proposed order)

| Batch | Content | Why this order |
|---|---|---|
| F1 | Finish 🎬 1: SH-032–034 (reuse the M01/M02 set, add M20 trolleys and M21 staff) and the UT 1 transition to SH-035 | The set already exists, so this makes the first complete 3D sequence |
| F2 | 2D asset library: A01 glass kit, A05 NOKAS façade, A10 type kit, A15 notebook (done), A17 clock/calendar, A13 maps | Reused in about 60 of the 87 2D shots |
| F3 | 🎬 2 "113": relight M01/M02 for daylight, glass-damage mask states, G01 counter | Reuses the 🎬 1 set |
| F4 | Cold open plus Ch. 1–2 in 2D (SH-001–027) | The hook decides retention, so it needs the most polish |
| F5 | 🎬 4 café (M12, M13, M19, M16) and Ch. 7 | Needs the period references checked first |
| F6 | 🎬 3 "The Windshield": the most restrained sequence, tested on an audience | Tone-critical |
| F7 | Remaining 2D chapters, then the sound pass, then the final narration lock and re-time |

## Known timing risks (from the TTS animatic)
See `01_SCRIPT_STORYBOARD/animatic/vo_timing_report.csv`. Shots flagged **OVERRUN** need a longer shot, a VO trim, or VO that runs across the cut (L-cut). Re-time them once the real narrator is recorded. Do not lock picture before that.

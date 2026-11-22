# Motion clips v001

**Model:** Higgsfield `seedance_2_0`, image-to-video, 5 s, 720p, `mode: fast`, no generated audio. **Cost:** 225 credits (18 clips at 12.5 credits each). No redos were needed. **Pilot 2** (22 Nov): 6 more clips on shots that were stills only, 75 credits, all passed QC.
**Start frames:** the approved stills from `02_VISUAL_DEVELOPMENT/shot_stills_v001` (job IDs in `jobs.tsv`).
**Check:** every clip was inspected at its start, middle and end (`qc/`). No warping, morphing or face reveals; the style holds.

| Clip | Shot | Motion |
|---|---|---|
| M_201 | 2.1 cathedral square | gulls, rising light |
| M_302 | 3.2 Toska at the chessboard | lamp breathing, figure still |
| M_501 | 5.1 through the glass | slow push-in, light shift |
| M_702 | 7.2 church | candle flicker |
| M_803 | 8.3 red alarm light | blink |
| M_905 | 9.5 coach bus | drives away |
| M_1001 | 10.1 townhouses | headlight sweep |
| M_1202 | 12.2 truck (v1, superseded by M_12022) | smoke rising, flames confined to the cab |
| M_12022 | 12.2 truck, redo from still SH_12022 (European cab-over) | smoke drifts, glow confined to the cab, slow push-in |
| M_102 | 1.2 courtyard (pilot 2) | slow push-in, haze, clouds |
| M_601 | 6.1 frost (pilot 2) | breath puffs, figure still, no face |
| M_1002 | 10.2 woods (pilot 2) | torch beams sweep, slight camera drift, figures still |
| M_1401 | 14.1 corridor (pilot 2) | push-in, fluorescent flicker |
| M_1601 | 16.1 square (pilot 2) | slow pan right, bus in the distance |
| M_2102 | 21.2 Oslo café (pilot 2) | CRT glow, slow drift |
| M_1304 | 13.4 the hole | dust |
| M_1402 | 14.2 lift | doors close (made from still 14.1) |
| M_1404 | 14.4 square | police car drives in |
| M_1704 | 17.4 sky | clouds |
| M_1802 | 18.2 woods | smoke column |
| M_1804 | 18.4 flat | TV flicker |
| M_1902 | 19.2 rooftops | helicopter |
| M_2101 | 21.1 village | heat haze |
| M_2202 | 22.2 police station steps | candles |
| M_2401 | 24.1 the intact glass | push-in, reflections |

**In the animatic:** each clip replaces its still (`build_stills_animatic.py`, which uses the `MOTION` map). A clip is slowed by up to 2× to fit its slot, and its last frame is held if the slot runs longer.

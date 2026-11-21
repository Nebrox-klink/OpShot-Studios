# Shot stills v001 (script v008)

**Model:** Higgsfield `nano_banana_2_1`, 2k, 16:9. The approved style references (`../style_refs_v001`) were passed as image references for consistency.
**Count:** 63 final stills (`final_jpg/S<scene>_<shot>.jpg`, numbered as in script v008; the chairs shot 7.3 has three stills, S07_31 to S07_33). **Cost:** 134 credits (67 generations at 2 credits each, including 3 redos and the 2 extra stills for the chairs shot).
**Masters:** the full-resolution PNGs are not in git (465 MB). Every one can be re-downloaded from the Higgsfield history using the job IDs in `jobs.tsv`. `final_map.tsv` shows which generation became each final still.

**Not made, on purpose:**
- **Edit-only shots:** the title, dates, maps, lower-thirds, the 08:08 clock, black and white frames.
- **The Klungland portrait (9.4 and 19.3):** waiting on the family's answer (gate G-FAM).
- **Shot 20.3:** reuses 14.2 (the closed lift doors).

**Redos (no-glorification and "Toska only from behind" rules):**
- **1.5 rifle:** the first take was a side-on aiming pose. Replaced with a static rear view, rifle held low.
- **6.1 and 22.3:** Toska's profile was partly visible. Replaced with rear views showing no face.

**Minor issues, acceptable for now; fix later if wanted:**

| Shot | Issue |
|---|---|
| 7.2 | The figure at the lectern faces the camera, but is small and has no facial detail. |
| 8.1 | A small walker appears in the underpass. |
| 10.4 | The watch is on a sweater cuff, not a glove. |
| 11.1 | The front row of officers shows partial side faces. The figure at the front stands in Klungland's role, but has no facial detail. |
| 12.1 | The security-camera street looks American, with fire escapes. |
| 12.2 / 18.3 | Truck types are generic, not a 2004 Volvo. |
| 16.2 | The police car looks American. |
| 22.4 | The two figures read as leaving rather than entering. |
| 23.1 | The hall looks like an old church hall. |

Everything is regenerable with `make_shot_prompts.py` (prompts) and `next.py` (queue).

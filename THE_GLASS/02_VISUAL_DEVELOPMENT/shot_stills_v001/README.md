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

**Redos, v002 (period and location fixes; 10 credits, plus 12.5 for the new 12.2 motion clip):**
- **12.1** (`SH_12012`, ref BG4): a Norwegian street of low white wooden houses, not an American one with fire escapes.
- **12.2** (`SH_12022`) and **18.3** (`SH_18032`): flat-fronted European cab-over truck, Volvo FH style. A small diagonal grille bar is visible; there is no readable badge.
- **16.2** (`SH_16022_clean`, ref BG3): a Volvo V70 estate with the blue and black chequered stripe. Faint pseudo-letters on one vest were painted out locally (the unedited master is `SH_16022`).
- **22.4** (`SH_22042`, ref 22.3): two backlit figures walk in toward the camera.
- The old JPGs are in `superseded/`.

**Minor issues, acceptable for now; fix later if wanted:**

| Shot | Issue |
|---|---|
| 7.2 | The figure at the lectern faces the camera, but is small and has no facial detail. |
| 8.1 | A small walker appears in the underpass. |
| 10.4 | The watch is on a sweater cuff, not a glove. |
| 11.1 | The front row of officers shows partial side faces. The figure at the front stands in Klungland's role, but has no facial detail. |
| 23.1 | The hall looks like an old church hall. |

Everything is regenerable with `make_shot_prompts.py` (prompts) and `next.py` (queue).

**Klungland shots (9.4 and 19.3), replaced at the producer's request:** instead of a portrait, each uses an anonymous officer in a 2004 Norwegian uniform, seen from behind with no face and no likeness. Captions are added in the edit:
- **9.4:** the officer beside a patrol car, with the lower-third "Arne Sigve Klungland".
- **19.3:** the officer walking away alone, with the caption "In memory of Arne Sigve Klungland · 1950 – 2004".

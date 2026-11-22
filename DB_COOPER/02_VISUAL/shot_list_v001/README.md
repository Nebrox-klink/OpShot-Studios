# D.B. Cooper: shot stills, round 1 (22 Nov 2026)

**Status:** 42 of 42 round-1 stills (scenes 1–14) checked and approved. Review copies are in `final_jpg/` (1280 px). The 2k PNG masters are in `stills/`, which is gitignored; they can be re-downloaded from Higgsfield using the job IDs in `jobs.tsv`. There is a contact sheet in `round1_contact_sheet.jpg`.

## Tools
- **Prompts:** `make_shot_list.py` is the source of the shot list and the prompts; it writes `requests_round*.json` in batches of 8.
- **Download:** `dl.sh ID URL` downloads a still and makes the review copy.
- **Contact sheet:** `sheet.sh OUT ID…` makes a labelled 640-px contact sheet for QC.

## Prompt changes made at submission (the sent text differs from `make_shot_list.py`)
- **1201:** the banknote is seen against the light, so its printing is only a soft green blur.
- **1202:** "racetrack sign" removed; all signs are blank.
- **1302–1305:** set in "February 1980"; the money is described as "old greenish paper money, printing washed out, no portraits/words/numbers" after the 303 failure.
- **1401 and 1403:** dated 1970s and 1960s.

## Redos (second attempt each; v1 moved to `superseded/`)
| Shot | v1 problem | Fix |
|---|---|---|
| 303 | Banknotes showed readable "UNITED STATES OF AMERICA / DOLLAR" | Money folded edge-on, plain green, no printing |
| 401 | Cooper's cheek and ear visible | Higher camera, directly behind; only the top and back of the head |
| 602 | Passengers read as walking *toward* the plane (boarding) | Passengers walk toward the camera, away from the plane |
| 1003 | A propeller cargo plane, but the narration says "the same type of plane" (727) | Unmarked 727 over jungle dropping a pallet |

## QC notes (accepted)
- **1201:** the teller (anonymous) is half in profile. The bill lettering is blurred and illegible at 1280 px; soften it further in the edit if needed.
- **603:** the pilot holds the handset up, which hides the face; only a small part of the cheek shows.
- **1102:** the loafer is on wet ground rather than in mid-air; it still works as an abstract cue for "suit and loafers".
- **1403:** small, anonymous engineers in white shirts.

## Cost
42 + 4 redos = 46 images × 2 = **92 Higgsfield credits**.

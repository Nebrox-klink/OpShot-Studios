# Yuba County Five: animatic v002 (25 Nov 2026)

`YUBA_animatic_v002.mp4` (720p, local only, gitignored), built by `../tools/build_animatic_v002.py`. Cut list with times: `YUBA_animatic_v002_cuts.txt`. 152 cuts, 8:42, narration only.

## What changed from v001 (producer's notes)
1. **The picture now follows the narrator.** v001 split each scene's time evenly by cut count, so pictures drifted away from the words (e.g. "the Gateway Gators" landed on the wrong image).
   - Every shot is anchored to the words it illustrates (`ANCHORS` in the builder).
   - `../tools/narration_timing.py` finds when each sentence is spoken from the pauses in Brian's read, and places a phrase inside its sentence by character position. This is accurate to about half a second inside long sentences.
   - Cut counts now follow each shot's length (about 3.4 s per cut, max 5.6 s).
2. **No snow inside the office.** The case-board shots (501, 1401) had the snow effect by mistake; they now get a light sweep and a lamp flicker.

## Re-ordered or repeated to match the words
- Scene 3: the jerseys come in on "the Gateway Gators"; the bags by the door on "still lived at home" and again on "laid out their uniforms".
- Scene 4: the car returns on "Jack Madruga drove".
- Scene 5: the phone comes before the case board.
- Scene 6: the skiers come on "People drove up that road in winter to ski".
- Scene 9: the lodge on "At dawn he walked…"; the empty car on "he passed the Mercury". The "8 MILES" label moved to the lodge.
- Scene 11: Ted's trailer room returns on "He died of starvation and cold".
- Scene 13: the empty floor opens the scene ("Ted's own shoes were missing"); the map returns on "All three…".
- Scene 14: the checklist comes on "No wounds", before the table.
- Scene 14: the bed returns on "Ted was wrapped in eight sheets".
- Scene 16: the tracks shot returns on "Its tracks led on up the road".
- Scenes 17–18: the lights and the fog each return for the closing lines.

Labels now appear on the first cut of their shot, at the moment the fact is said.

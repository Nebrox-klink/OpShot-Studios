# THE GLASS: Higgsfield workflow for the 4 cinematic scenes (v001)

This follows the workflow from the "Claude Blender kurs" videos (part 1 and 2), applied to our four 30-second 3D sequences.

**The course pipeline:**

```
Blender blockout (low-poly scene + animated camera)
  → render a REFERENCE VIDEO of the camera move
  → take a still from it → Nano Banana Pro: "turn this low-poly scene into a cinematic still" = VISUAL ANCHOR
  → (character sheet if a character appears)
  → Claude writes the Seedance 2.5 prompt (beat sheet + @Video1 / @Image refs)
  → Seedance 2.5: Draft first (480p, 10 s), then the full 30 s at 1080p
```

The course's **advanced workflow** has Claude build the Blender scene through an MCP connection. That is what we already did: the four blockouts were built by script in `05_BLENDER/scripts/` and rendered to `06_AI_VIDEO/references/`. **So steps 1–2 are done.** Steps 3–5 happen in Higgsfield on your account.

---

## Files ready for upload (`06_AI_VIDEO/references/`)

| Sequence | Reference video (@Video1) | Anchor sources (for Nano Banana) |
|---|---|---|
| 3D 1 "Through the Glass" (03:50–04:20) | `SEQ1_through_the_glass_REFVIDEO_30s.mp4` | `SH-031`, `SH-032`, `SH-033`, `SH-034` `_anchor_source.png` |
| 3D 2 "113" (06:15–06:45) | `SEQ2_113_REFVIDEO_30s.mp4` | `SH-050`, `SH-051`, `SH-052` |
| 3D 3 "The Windshield" (08:15–08:45) | `SEQ3_windshield_REFVIDEO_30s.mp4` | `SH-064`, `SH-065`, `SH-066`, `SH-067` |
| 3D 4 "One Year to the Day" (10:35–11:05) | `SEQ4_malaga_cafe_REFVIDEO_30s.mp4` | `SH-083`, `SH-084`, `SH-085`, `SH-086` |

Each reference video is exactly 30.0 s, 1280×720, 24 fps, with no sound. Its timing matches the edit, so Seedance's output drops straight onto the timeline.

## Rules that apply to every generation (from the production brief)
- **Anonymous figures only.** Robbers, police officers, staff and Toska are never shown with a recognisable face. No real person's likeness, and no photos of real people as references.
- **No gore and no glorification.** No blood, no wounds, no visible guns or muzzles. Gunfire appears only as abstract light pulses. The robbers are never heroic: no slow-motion "cool" poses and no hero lighting.
- **Klungland (3D 3)** is shown with dignity: only hands and sleeve, never the head, never the moment of being hit. The crack is a symbol, not a bullet hole.
- **No readable text, logos or police markings** in any generated image (avoids invented signage and trademarks).
- **Málaga is an ordinary city street by the railway station** (Chicoti internet café). No beach, no seafront, no palm promenade.

---

## STEP 3: Visual anchors (Image → Nano Banana Pro, 16:9)

Upload the anchor source PNG as @image1. Use the course's prompt pattern, then generate 2–4 options and keep the best one per sequence. One anchor per sequence is enough; course part 2 used one per location.

**3D 1 (use SH-032 or SH-031):**
```
Change @image1, this low-poly scene of a night-time inner courtyard of a Norwegian cash depot, into a photorealistic cinematic still. Keep the exact camera angle, composition, window position and light directions. Night, frost on dark cobblestones, a 9 m plaster wall, one large window of thick laminated security glass glowing warm amber from the room behind, a cold blue-white wall lamp on the right. An anonymous hooded figure crouches against the wall below the window, back to camera, no face visible. Shot on 35 mm film, ARRI Alexa look, shallow depth of field, subtle film grain, cold teal shadows versus warm amber interior. No text, no logos, no weapons.
```

**3D 2 (use SH-050 or SH-051):**
```
Change @image1, this low-poly scene, into a photorealistic cinematic still seen from INSIDE a cash-counting room, looking out through a large window of thick laminated security glass at grey overcast early-spring morning light. Keep the exact framing. The glass is covered in white star-shaped impact marks and is turning milky; it has not broken. Behind the glass only blurred dark shapes, no faces, no weapons. Fluorescent-lit counting tables in the foreground, out of focus. Documentary realism, 50 mm, muted colours, fine film grain. No text, no blood.
```

**3D 3 (use SH-067, then SH-064 for the cabin):**
```
Change @image1, this low-poly scene, into a photorealistic cinematic still through the windshield of an early-2000s Norwegian estate car on a quiet Stavanger street at 8 a.m.: white wooden and plaster houses, wet asphalt, low warm morning sun, dust in the light beams, a cathedral spire in soft haze at the end of the street. A symbolic spider-web crack in the windshield, upper right. No people, no cars moving, no police markings, no text. Quiet, respectful, still. 70 mm, natural grade, no lens flares.
```

**3D 4 (use SH-084 or SH-083):**
```
Change @image1, this low-poly scene, into a photorealistic cinematic still inside a small 2005 internet café in Málaga, Spain: rows of beige PC towers and CRT monitors, plastic chairs, fluorescent ceiling panels, bright Mediterranean afternoon sun through the shop window onto an ordinary city street with 5-storey ochre and off-white plaster buildings and balconies (no sea, no beach, no palm promenade). A man in a light jacket sits at a PC, seen from behind, no face visible; the screen shows an unreadable news page. Keep the exact framing. 50 mm, documentary realism, film grain. No readable text or logos.
```

---

## STEP 4: Seedance 2.5 prompts (Video → Seedance 2.5, 30 s, 16:9)

**Upload:** the reference video as **@Video1** and the visual anchor as **@Image1**.

**Settings (from the course):**
- First run **Seedance 2.5 Draft, 10 s, 480p**. That showed as **30 credits** in the course video.
- If the motion is right, run the full **30 s, 1080p, bitrate High**. That showed as **480 credits**.
- Check your own price in Higgsfield before generating; these are the course's numbers.
- **Audio:** turn it ON only if you want ambience. Our narration and music come from the Resolve mix, so no dialogue is wanted in any shot.

### 3D 1: "Through the Glass" (30 s)
```
[GOAL]
A cinematic, photorealistic, 30-second night sequence in one continuous mood: an anonymous man waits in the frozen courtyard of a cash depot, watches through thick security glass as the money he came for is wheeled away, and silently gives up. Tense, quiet, cold. Documentary-drama realism, not an action film.

[REFERENCES]
@Video1 defines the camera choreography, timing, cuts, spatial blocking and the positions of every object and figure. Match it exactly. It is a low-poly blockout: do NOT reproduce polygonal characters or simplified graphics; render everything photorealistic.
@Image1 defines the look: the courtyard, the warm amber window, the cold wall lamp, the frost, the colour grade.

[BEATS]
0–7 s: Slow crane down from above the parapet to just behind the crouching hooded figure; the lit window fills the upper frame.
7–15 s: Over his shoulder, focus on the glass surface. Behind it, out of focus, two staff silhouettes wheel cash trolleys with grey bags from right to left and out through a doorway. A faint reflection of his hood on the glass.
15–22 s: Extreme close-up on the outer glass. His breath fogs the glass in three soft exhales; a gloved hand slowly closes into a fist in the lower left. The room behind is pure amber bokeh.
22–30 s: Static medium-wide. He lowers his head, stands stiffly and walks left into darkness without looking back. Slow push-in until the fading breath-fog patch fills the frame.

[CONSTRAINTS]
No faces visible on anyone. No weapons, no tools. No text. No running. Calm, defeated. Cold teal night versus warm amber interior, subtle film grain, 35 mm.
```

### 3D 2: "113" (30 s)
```
[GOAL]
A cinematic, photorealistic, 30-second sequence seen almost entirely from INSIDE a cash-counting room as attackers outside try to break through a window of thick laminated security glass. The glass is the protagonist. Frightening through sound and light, never through violence on screen.

[REFERENCES]
@Video1 defines the camera choreography, timing, cuts, framing and the progression of damage on the glass. Match it exactly. It is a low-poly blockout: do NOT reproduce polygonal shapes or the graphic star decals; render real impact marks in laminated glass.
@Image1 defines the room, the glass, the grey morning light and the grade.

[BEATS]
0–8 s: Locked 50 mm from inside. Blurred dark shapes outside. A heavy ram strikes the pane three times; the glass bows and settles, the first white impact stars appear, the room lights flicker, dust falls from the frame. The pane does not break.
8–20 s: Locked extreme close-up on the pane, no camera movement. Bursts of new white star-shaped impacts appear in four steps; outside, only brief irregular warm light pulses (never show guns or muzzle flashes). The glass slowly turns milky. Keep the lower right corner calm and dark.
20–30 s: Slow motion. The glass sags inward like wet paper and a ragged hole opens at the lower centre; one black gloved hand and forearm reach through (no body, no weapon). The camera slowly dollies back into the empty counting room. End on a glass shard in the left foreground reflecting the room.

[CONSTRAINTS]
No faces, no visible weapons, no muzzle flashes, no blood, no people inside the room. No text or numbers in frame. Not heroic: no glamour lighting on the attackers. Muted documentary colours, 50–70 mm, film grain.
```

### 3D 3: "The Windshield" (30 s): handle with the most care
```
[GOAL]
A cinematic, photorealistic, 30-second memorial sequence: a police officer drives toward the incident on a quiet morning street; the moment of his death is shown only as a symbolic crack spreading through the windshield and a cut to white. Quiet, warm, dignified, respectful. This is a tribute, not an action scene.

[REFERENCES]
@Video1 defines the camera choreography, timing, cuts and composition. Match it exactly. It is a low-poly blockout: do NOT reproduce simplified graphics; render a real car interior and a real street.
@Image1 defines the street, the morning light and the grade.

[BEATS]
0–8 s: Fixed side profile inside the car cabin, 50 mm. Only the driver's hands on the steering wheel and a dark uniform sleeve are visible, never the head or face. Sun streaks slide across the dashboard; gentle road vibration. Calm.
8–16 s: POV from just behind the windshield as the car slowly turns into the street; smoke rises far ahead. Rack focus from dust on the glass to the street. Very still at the end.
16–20 s: Locked extreme close-up of the windshield glass only. A spider-web crack grows in three quick steps from a point upper right. No hole, no fragments, no hands, no person. Cut to pure white.
20–30 s: Hold white, then slowly fade up to the quiet empty street through the cracked windshield: morning sun, dust in the light beams, the cathedral spire in haze. No people, nothing moving. Extremely slow push-in, ending perfectly still.

[CONSTRAINTS]
Never show the officer's head or face, any wound, blood, shooter or weapon. No police markings, no text. No lens flares, no dramatic grading. Natural, warm, quiet.
```

### 3D 4: "One Year to the Day" (30 s)
```
[GOAL]
A cinematic, photorealistic, 30-second sequence: on an ordinary afternoon in Málaga a man sits at a computer in a small internet café near the railway station; plain-clothes police officers walk in calmly and the search is over. Anticlimactic, quiet, inevitable.

[REFERENCES]
@Video1 defines the camera choreography, timing, cuts and the blocking of every figure. Match it exactly. It is a low-poly blockout: do NOT reproduce box-shaped figures; render real people, a real 2005 café and a real street.
@Image1 defines the café, the light and the grade.

[BEATS]
0–7 s: Slow dolly along an ordinary sunny Málaga street (plaster buildings, balconies, parked mid-2000s cars) toward the café's glass door.
7–13 s: Locked over-the-shoulder on the seated man, seen from behind, no face. The CRT screen shows an unreadable news page.
13–22 s: Rack focus from the screen to the entrance: three or four plain-clothes officers in jeans and jackets walk in from the left, calm and unhurried. The man stays seated. No struggle.
22–30 s: Locked extreme close-up on the CRT screen as it switches off to black; a faint reflection of the room in the dark glass.

[CONSTRAINTS]
No faces visible on the seated man or the officers. No sea, beach or palm promenade. No readable text, signs or logos. No guns drawn, no chaos, no shaky action camera. Bright Mediterranean light outside, cool fluorescent inside, documentary realism, film grain.
```

---

## STEP 5: Into the edit
1. Export each Seedance result as `SH-031.mp4`, `SH-050.mp4`, `SH-064.mp4` and `SH-083.mp4`: the first shot ID of each sequence, because each video covers the whole 30 s.
2. Put them in `THE_GLASS\06_AI_VIDEO\approved\`.
3. Run **Workspace → Scripts → Utility → THE_GLASS_resolve_master_v003** in Resolve.

The script places each file at its sequence start on V2. With `HIGGSFIELD_SEQUENCE_MODE = True` (the default), a clip named after the first shot of a sequence fills the whole 30 s; set it to False to trim each clip to one shot instead.

## Cost overview (course prices, not yet checked on your account)

| Step | Count | Credits each | Total |
|---|---|---|---|
| Nano Banana Pro anchor | 4–8 | check in app | — |
| Seedance 2.5 Draft 10 s 480p | 4–8 | 30 | 120–240 |
| Seedance 2.5 30 s 1080p | 4 | 480 | 1,920 |

**Total: about 2,100–2,200 credits plus the anchors** for all four sequences, if every final generation works on the first try.

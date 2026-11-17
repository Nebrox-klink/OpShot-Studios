# THE GLASS: Blender prompts for the 3D cinematic scenes (v001)

There are four 3D sequences. Each lasts 30 seconds, and together they make 15 shots. They follow script v004 and storyboard v1.1.

## How to use these prompts

Each prompt in a grey box is written to be pasted into an AI assistant that can control Blender. Examples are Claude Desktop with a Blender MCP connector, or Claude Code running `blender -b -P` or the `bpy` module. They also work as a written brief for a human 3D artist.

1. **Paste the MASTER PROMPT first** in every new session. It fixes scale, palette, file names, render settings and the ethics rules.
2. Then paste **one set prompt** (S1–S4), which builds or opens the shared set, and after it **one shot prompt at a time**.
3. After each shot, ask for a test still before the full render (the master prompt already requires this).
4. SH-031 is **already built**: `05_BLENDER/scripts/build_SH031_courtyard.py`. Prompts S1 and SH-031 tell the assistant to reuse that script, not rebuild it.

All coordinates are in metres. +Y points from the camera side of the courtyard toward the NOKAS wall. Z is up. The frame rate is 24 fps.

---

## MASTER PROMPT (paste first)

```text
You are the Blender technical director for "THE GLASS — The NOKAS Robbery", an animated
documentary about a real robbery in Stavanger, Norway, in 2004, in which a police officer
(Arne Sigve Klungland) was killed. Work in Blender 4.2+ (5.x is fine) through Python (bpy).
Write every step as a reusable script saved in THE_GLASS/05_BLENDER/scripts/, then run it.

TECHNICAL BASELINE (target laptop: Intel i7, 16 GB RAM, integrated Intel GPU, no CUDA)
- Render engine EEVEE. 24 fps. Preview 960x540 or 1280x720, final 1920x1080.
  16 samples for previews, 32 for finals. Raytracing OFF. No fluid, smoke or particle
  simulations. No volumetrics unless I ask.
- Low-poly geometry. Procedural materials only, with no external textures. Use instances for repeats.
- Colour management: AgX, look "AgX - Base Contrast", exposure about +0.9 for night scenes.
- Glass: NEVER use transmission or refraction (it renders black on this hardware). Use
  2–3 thin alpha-blended layers (alpha ~0.16, base colour #6B9483 tint, roughness 0.08)
  that read as thick laminated security glass.
- Use bpy.ops.object.transform_apply(location=False, rotation=False, scale=True) only.
  The default also applies location and rotation and breaks parenting.

PALETTE (linear-ish values)
- Night navy #17212B (world/background), slate #556774 (walls), ivory #E9E6DE,
  amber #C78B55 (the ONLY warm accent: money / the lit window / the cash room),
  oxide red #A95149 (never decorative), glass green #78A08C.
- 3D sequence 4 (Málaga) alone uses warm sun #E8C27A.
- Rule: warm amber = the target/money. Cold blue = outside world, night, police.

STYLE
- Stylised, grounded, cinematic, slightly desaturated. Not photoreal, not cartoon.
- People are faceless low-poly silhouettes in dark matte cloth (rough 0.9, base ~0.02).
  Every dark figure gets a cold rim light, or it vanishes against dark walls.
- Cameras behave like physical rigs (crane, dolly, tripod, restrained handheld) with 24–85 mm
  lenses. Use Bezier easing with AUTO handles, and no impossible moves.

ETHICS AND HISTORY (hard rules)
- No faces, no identifiable likeness of real people, no blood, no wounds, and never the
  moment of impact on a person. No weapon glamour shots.
- Glass is the recurring motif. Each sequence begins and ends on a glass surface, so the
  2D animation can match-cut into and out of the first and last frames.
- Everything not documented is a "dramatised reconstruction". Keep it neutral. Never
  invent extra action (no chases, no struggles, no extra people).
- No readable text inside renders. Dates and numbers are added in 2D compositing.

FILES AND NAMING
- Scene file: THE_GLASS/05_BLENDER/sequences/<SHOT>_<name>_v###.blend
- Frames:     THE_GLASS/05_BLENDER/renders/<SHOT>/<SHOT>_####.png (start at frame 1)
- Preview:    THE_GLASS/05_BLENDER/renders/<SHOT>_preview_v###.mp4 (ffmpeg, H.264, yuv420p)
- Also export the FIRST and LAST frame as <SHOT>_ref_frame_first.png / _last.png
  (these are the 2D match frames).
- Store custom properties on the scene: shot_id, sequence, source_class.

WORKFLOW FOR EVERY SHOT
1. Build or open the set. 2. Animate. 3. Render 3 test stills (first, middle and last frame)
at 960x540, look at them, and report problems honestly: black glass, invisible figures,
noise, framing. 4. Fix. 5. Only then render the full frame range. 6. Report the render time
per frame and the output paths. Never say a render is done or verified unless you have
opened and inspected the output.
```

---

## SEQUENCE 3D 1: "THROUGH THE GLASS" (03:50–04:20)

*Fact basis: in February 2004 Toska waited in the NOKAS courtyard, saw through the window that money was being moved out of the basement, and called the robbery off (S04, S05). The weather, light and blocking are dramatised.*

### S1: Set prompt, NOKAS courtyard (M01/M02/M06), shared with 3D 2

```text
Open or build the shared NOKAS courtyard set. If THE_GLASS/05_BLENDER/scripts/
build_SH031_courtyard.py exists, run it and reuse its geometry, materials and lights exactly.
Do not rebuild them. Otherwise build this:

- Courtyard floor 11 m (X) x 9 m (Y), centred at the origin. Cobblestone ground with a
  procedural noise colour, dark grey-blue, plus a SUBTLE frost mask (small-scale noise,
  frost colour only slightly lighter than the ground: it must not read as camouflage).
- Walls 9.5 m high, 0.45 m thick. The back wall (the NOKAS façade) has its inner face at y = +4.5.
  Side and front walls are darker plaster. Add parapets, a string course at z = 3.6,
  a steel service door at x = -3.6, a drainpipe at x = -1.6, a utility box at x = 4.2 and one bin.
- WINDOW (M02): centre x = +0.6, sill height 0.9 m, opening 2.2 m wide x 1.6 m high, steel frame
  with a centre mullion, three alpha-blended laminated glass layers 3 cm apart. This window
  is the hero object of the film, so name it M02_window and keep its transform fixed
  forever (3D 2 reuses it).
- ROOM BEHIND (M06): a closed box 6 m x 4.2 m x 3 m behind the window, warm amber walls
  (emission ~0.9), a ceiling light panel, a shelf, a table, two amber point lights inside.
- Lights: an area light behind the glass pointing into the courtyard (amber, ~520 W,
  rotation X = -90°), a cold wall lamp at x = 3.0 (spot, ~260 W, pale blue), and a weak blue
  moonlight sun (0.35).
- Name collections: SET_courtyard, SET_window, SET_room, LIGHTS_night.
Save as 05_BLENDER/shared_assets/M01_courtyard_set_v001.blend and render one test still.
```

### SH-031 · 7 s · frames 1–168 (BUILT, render v001 exists)

```text
SH-031, 3D 1 "Through the Glass", opening shot, 7 s (168 frames).
Reuse 05_BLENDER/scripts/build_SH031_courtyard.py. It already contains this shot.
If rebuilding:
- Figure M03b: one anonymous hooded figure crouched with its back to the camera, hugging its
  knees, against the wall just left of and below the window (root at x = -0.55, y = 3.95).
  Build it from bevelled boxes and an ellipsoid hood. No face. Breathing: torso X/Y scale
  1.00→1.03→1.00, period ~3.3 s. Cold rim light from the right, plus a soft blue back fill.
- Camera crane (Track-To an empty on the window), Bezier:
  f1   (-3.8,-3.6,10.6) 24 mm, looking down from above the front parapet
  f60  (-3.0,-2.3, 7.4) 26 mm
  f120 (-2.2,-0.9, 3.0) 29 mm
  f168 (-1.75,0.95,1.42) 32 mm, low over the figure's left shoulder, the lit window filling the
  upper middle of the frame. DOF on the figure, f/4.
- No music cue in Blender. Frame 1 must be exportable as the 2D match frame.
```

### SH-032 · 8 s · frames 1–192

```text
SH-032, 3D 1 "Through the Glass", 8 s (192 frames). Open the M01 set and the SH-031 figure.
Shot: over-the-shoulder through the thick laminated glass. Behind it, out of focus, two
anonymous staff silhouettes (M21: simple capsule figures, warm-lit, no faces) slowly
wheel two cash trolleys (M20: low-poly trolleys with 4–6 grey bags) from the right side
of the room to the left and out of view through a doorway.
- Camera: 50 mm, positioned 0.6 m behind and 0.3 m above the figure's right shoulder, aimed at
  the window centre. Focus distance on the GLASS SURFACE (so the room behind is soft), f/2.8.
  Almost static: a 10 cm dolly-in over the whole shot.
- Staff walk speed about 0.5 m/s. They enter at f20 and exit by f170. Trolleys follow with a slight lag.
- Add a faint reflection of the figure's hood on the glass (a duplicate layer with low
  alpha, or a screen-space reflection plane).
- No weapons, no tools, no other people. The staff must stay unrecognisable blur.
Deliver a first/last ref frame. Last frame: the room is empty, the trolleys are gone.
```

### SH-033 · 7 s · frames 1–168

```text
SH-033, 3D 1 "Through the Glass", 7 s (168 frames). VO over this shot: "Through the glass,
he watched the money being moved away."
Shot: extreme close-up (85 mm) on the outer glass layer at the height of the figure's face.
His breath fogs the glass: an animated condensation patch (a plane just in front of the glass,
white-blue, alpha driven by a radial gradient × noise), growing with each exhale
(f20, f75, f130) and fading between them. In the lower left of the frame, his gloved hand
(a simple mitten shape is fine) closes slowly into a fist between f90 and f150.
The warm room behind is completely defocused into amber bokeh.
- Camera locked on a tripod, f/2, focus on the glass. Cold rim light on the hand.
- The fog must never look like a crack. Keep it soft and round.
```

### SH-034 · 8 s · frames 1–192

```text
SH-034, 3D 1 "Through the Glass", 8 s (192 frames). VO: "He called it off."
Shot: medium-wide, static, slightly lower than the window sill. The figure lowers its head
(f10–f40), stands up stiffly (f40–f90) and walks left out of frame into darkness (f90–f140).
The camera stays on the window. The last breath-fog patch on the glass fades slowly.
From f120, a slow digital push (lens 50→85 mm) ends with the fading fog patch filling the frame.
- The last frame (f192) is the 2D match frame: the soft fog patch, centred, on dark glass with
  amber bokeh. It becomes an eraser smudge over "FEB 2004" in the 2D notebook.
- No running and no looking back. Calm, defeated, quiet.
```

---

## SEQUENCE 3D 2: "113" (06:15–06:45)

*Fact basis: on 5 April 2004 at about 08:00 the robbers broke in through the courtyard window using a sledgehammer and a battering ram. Sources (secondary) say 113 shots were fired into the window. Toska had believed it was ordinary glass (S04). The choreography and the glass physics are dramatised. The 113 figure needs confirming against the court ruling.*

### S2: Set prompt, relight M01 for daylight + damage states for M02

```text
Open 05_BLENDER/shared_assets/M01_courtyard_set_v001.blend. Do NOT move any geometry.
1. Create a second light setup in a new collection LIGHTS_morning and disable LIGHTS_night:
   overcast early-spring morning at 08:00. Soft cool sky (world colour ~#8A99A6, strength 1.2),
   a weak sun (1.5) from upper left, slightly warm. The window room stays warm but much less dominant.
   Remove the frost. Make the ground damp (roughness 0.5).
2. Build M02 damage states as material/mask variants on the OUTER glass layer, switched by
   one custom property "damage" (0–4) that drives a Mix shader:
   0 intact · 1 a few white star impacts · 2 many stars · 3 dense crazing, glass milky ·
   4 the pane sagging inward (shape key "sag": centre pushed 25 cm into the room, edges
   held by the frame).
   Draw the impact stars as procedural decals (a radial line pattern plus a white core).
   Place them pseudo-randomly with a fixed seed. Do NOT simulate ballistics.
3. Add M06 counting-room detail behind the window: tables, a sorting-machine block, a shelf
   with grey bags. Keep it low-poly.
Save as M01_courtyard_set_morning_v001.blend.
```

### SH-050 · 8 s · frames 1–192

```text
SH-050, 3D 2 "113", 8 s (192 frames). Start frame must match the 2D frame SH-049 (a masked
silhouette raising a sledgehammer in front of the pane), so frame 1 frames the window
frontally from inside the counting room. This is the same angle as the SH-032 window, but
reversed, looking out.
Shot: from INSIDE the counting room, locked 50 mm, the window fills ~60% of the frame. Outside,
blurred dark silhouettes (M03, 2–3 masked figures, no faces, no visible weapons). A battering
ram (M05, a simple heavy cylinder with handles) strikes the pane at f30, f80, f130. On each hit
the glass bows (shape key "sag" pulses to 0.25 and settles) and damage steps 0→1→2.
A small camera shake on each hit (2 frames, a few millimetres).
- Room lights flicker slightly on each impact. Dust motes (a few planes) fall from the frame.
- The pane must NOT break in this shot.
```

### SH-051 · 12 s · frames 1–288

```text
SH-051, 3D 2 "113", 12 s (288 frames). Locked extreme close-up from inside, 70 mm, no camera
movement at all, centred on the pane.
Damage grows from state 2 to state 3 in 4 clear steps (f1, f70, f140, f210). Each step adds
a burst of new white stars. Muzzle flashes outside are ONLY abstract light pulses: a warm
point light outside the glass flickering for 1–2 frames, 12–16 pulses spread across the shot,
irregular. Never show guns or muzzles.
- Leave the bottom-right 20% of the frame calm and dark: the 2D "113" counter is composited
  there later (never render numbers in Blender).
- The glass slowly turns milky (mix toward an ivory haze) as the damage grows.
```

### SH-052 · 10 s · frames 1–240

```text
SH-052, 3D 2 "113", 10 s (240 frames). VO: "One hundred and thirteen shots. And finally…
the glass gives."
Shot: slow motion. The pane is at damage state 4. The "sag" shape key goes 0.25 → 1.0 between
f30 and f150 with ease-in. The glass does not shatter: it folds inward like wet paper and a
ragged hole opens at the lower centre (animate a boolean or an alpha mask growing from the
centre). At f150–f200 one black gloved hand reaches through the hole (only the hand and
forearm, no body, no weapon).
- Camera: slow dolly BACK into the counting room, 55 mm, from 1.2 m to 3.5 m away from the window,
  f1→f240, with a slight rise.
- Last frame (2D match OUT 2): a large glass shard in the foreground at the left (a separate
  plane) carries a sharp reflection of the room. The 2D counting room starts from that reflection.
- No staff visible in this shot.
```

---

## SEQUENCE 3D 3: "THE WINDSHIELD" (08:15–08:45)

*Fact basis: police lieutenant Arne Sigve Klungland was in a police command vehicle and was killed by a shot to the head (S01). Everything else (route, angle, windshield) is SYMBOLIC. This is the most restrained sequence in the film. It must have NO violence on screen, NO blood, NO impact on a person, and NO face. There is no narration during this scene.*

### S3: Set prompt, command-vehicle cabin + street (M07–M11)

```text
Build a new scene "S3_windshield":
- M07 car cabin of an early-2000s Norwegian police command vehicle (a generic estate/van
  interior: dashboard, steering wheel, two front seats, A-pillars, windshield with a slight
  curve). Low-poly. Do NOT add police markings or text.
- M08 driver: an anonymous partial figure. Only the hands on the wheel, the forearms in a dark
  uniform sleeve, and the shoulder edge are ever visible. No head or face is ever in frame.
- M10 street: one Stavanger-like city street seen through the windshield (2–3-storey white
  wooden and plaster façades as simple blocks), wet asphalt, morning light. Distant smoke
  as 2–3 soft alpha cards (no simulation).
- M11 the cathedral spire as a simple silhouette in the haze at the end of the street.
- Light: warm low morning sun from front left through the windshield (sun 3.0, #F2D3A0),
  cool sky fill. Dust in the light beam as a few small alpha planes.
- Windshield crack: a separate decal plane with a procedural "spider-web" crack mask,
  controlled by a property "crack" 0→1 (radial lines growing from a point upper right of
  centre). It is a GRAPHIC symbol. It has no physics and no hole.
Save as 05_BLENDER/shared_assets/S3_windshield_set_v001.blend.
```

### SH-064 · 8 s · frames 1–192

```text
SH-064, 3D 3 "The Windshield", 8 s (192 frames). Frame 1 must match the 2D portrait
reflection in the car's side window (2D SH-063), so start on the side window glass.
Shot: fixed side profile inside the cabin, 50 mm, camera on the passenger side looking toward the
driver's side window and the windshield edge. Only the HANDS on the wheel and the sleeve are visible.
Calm, warm, dignified: sun streaks slide across the dashboard as the car drives (animate the
sun rotation slightly, and add a gentle vibration of 2–3 mm to the cabin, not the camera).
- Focus on the hands, f/2.8. Nothing dramatic happens in this shot.
```

### SH-065 · 8 s · frames 1–192

```text
SH-065, 3D 3 "The Windshield", 8 s (192 frames).
Shot: POV from just behind the windshield, 35 mm. The car turns slowly into the street
(the camera yaws about 12° over the shot and moves forward ~6 m). Smoke rises ahead.
Far ahead at a corner, a single indistinct dark silhouette stands at the edge of the frame,
small, out of focus, never sharp, and never clearly holding anything.
Rack focus: f1–f100 sharp on the windshield (dust and reflections), f100–f170 shifting to the street.
- If in doubt, leave the silhouette out entirely. The smoke alone is enough.
- The final frames (f170–f192) are very still.
```

### SH-066 · 4 s · frames 1–96

```text
SH-066, 3D 3 "The Windshield", 4 s (96 frames).
Shot: locked extreme close-up of the windshield glass only, 70 mm, with the street soft behind it.
The crack decal "crack" animates 0 → 1 in three quick steps (f20, f26, f32), growing from a
point upper right of centre into a spider web. The cabin does not move. No hole, no fragments,
no hands, no person visible.
At f60 cut to pure white: set the world to white, the exposure up, everything white,
holding to f96 (the white continues into SH-067).
```

### SH-067 · 10 s · frames 1–240

```text
SH-067, 3D 3 "The Windshield", 10 s (240 frames).
Shot: starts pure white (f1–f40) and slowly fades (f40–f140) to the view through the
symbolically cracked windshield: an empty, quiet street, morning sun, dust drifting through
light beams, the cathedral spire in haze at the end of the street. No people, no cars moving.
Camera: extremely slow push-in, 70 mm, 0.4 m over 240 frames, ending perfectly still.
- Last frame (2D match OUT 3): the cracked glass in the foreground holds the frame. The 2D
  memorial card starts from that glass texture.
- The tone is quiet and respectful. No lens flares, no dramatic grading.
```

---

## SEQUENCE 3D 4: "ONE YEAR TO THE DAY" (10:35–11:05)

*Fact basis: Toska was arrested at the internet café Chicoti in Málaga, a little over 100 m from the railway station. He had been there about 10 minutes when a handful of police officers came in and arrested him at a computer, and he surrendered immediately without resistance (S06–S10). The date is reported as 5 April 2005, though some outlets say 6 April. The façade, the interior and all blocking are a GENERIC reconstruction, not a copy of the real café. No seafront and no coffee cup.*

### S4: Set prompt, Málaga street + internet café (M12–M14, M16, M19)

```text
Build a new scene "S4_malaga":
- M12 street: an ordinary Málaga city street in 2005, near a railway station (no beach, no
  palms on the promenade, no sea). 4–6-storey plaster façades in warm off-white and ochre,
  balconies, shutters, ground-floor shopfronts. Narrow pavement, asphalt road.
- M14 props: 2–3 period-correct parked cars (generic mid-2000s hatchbacks/sedans as low-poly
  blocks), a street light, a couple of plain signs with NO readable text.
- M13 internet café: a ground-floor shopfront with a generic sign (a blank or abstract graphic,
  no letters), a glass door, a window. Interior: 6–8 desks in rows, beige PC towers,
  CRT monitors (M19, deep backs, curved screens), keyboards, mice, plastic chairs,
  fluorescent ceiling panels, a small counter near the door.
- Light: bright Mediterranean afternoon sun (sun 4.0, #E8C27A, high angle) outside. Inside,
  cool fluorescent fill plus the sun through the window. CRT screens glow faintly blue-white
  with an unreadable abstract "news page" texture (blocks and lines, no letters).
- M03b: the same anonymous figure language as 3D 1, but seated, in a light jacket, back to
  the camera, no face. M16: 3–4 plain-clothes police figures (jeans, jackets, faceless).
Save as 05_BLENDER/shared_assets/S4_malaga_set_v001.blend.
```

### SH-083 · 7 s · frames 1–168 (4A)

```text
SH-083, 3D 4 "One Year to the Day", shot 4A, 7 s (168 frames). Frame 1 must match the 2D
glare (SH-082): start slightly overexposed (exposure +2 → normal by f24) so the cut from the
2D photo glare is seamless.
Shot: establishing street shot, 35 mm, a slow dolly toward the café entrance (~4 m forward,
slight right drift) at eye level. 2–3 pedestrians cross in the background at normal walking pace.
Ordinary daily life, nothing ominous on screen.
```

### SH-084 · 6 s · frames 1–144 (4B)

```text
SH-084, 3D 4 "One Year to the Day", shot 4B, 6 s (144 frames). VO: "The fifth of April, 2005."
Shot: inside the café, a locked over-the-shoulder shot of the seated figure (M03b) at a CRT, 50 mm.
The screen shows an abstract, unreadable news layout. Subtle CRT flicker (emission ±5% at
irregular frames). Fingers on the keyboard: small key-press motion only.
- Leave the upper right third of the frame calm: the date graphic "5 APRIL 2005" is added
  in 2D. Never render text.
```

### SH-085 · 9 s · frames 1–216 (4C)

```text
SH-085, 3D 4 "One Year to the Day", shot 4C, 9 s (216 frames).
Shot: rack focus from the CRT screen (f1–f60, sharp) to the café entrance (f60–f100). The glass
door opens at f70. 3–4 plain-clothes officers (M16) enter calmly at walking speed and spread
slightly (f80–f160). The seated figure turns his head toward them (f120–f150) and STAYS
SEATED. No raised hands, no handcuffs, no weapons drawn, no running. Other café users are
absent or blurred, and they do not react dramatically.
- Camera: 40 mm, tripod or very slow drift, NOT handheld chaos.
```

### SH-086 · 8 s · frames 1–192 (4D)

```text
SH-086, 3D 4 "One Year to the Day", shot 4D, 8 s (192 frames).
Shot: locked extreme close-up of the CRT monitor, 70 mm. At f30 the screen switches off
(emission fades to 0 over 6 frames, with a brief white horizontal line collapse typical of CRTs).
In the now-dark curved glass, a reflection appears (from a mirror-like glass material on
the screen: roughness 0.05, dark base): the silhouette of the seated man and the standing
officers behind him, soft and faceless, visible f60–f150, then fading slightly.
- Last frame (2D match OUT 4): the dark screen with the faint reflection, centred. The 2D
  identification card "DAVID TOSKA — ARRESTED — MÁLAGA" starts from that reflection.
- Render a separate pass with only the reflection (view layer or holdout) for compositing.
```

---

## Quick reference: frame ranges and match frames

| Shot | Sequence | Length | Frames | Match frame |
|---|---|---|---|---|
| SH-031 | 3D 1 | 7 s | 1–168 | **IN 1**: f1 under the 2D shards |
| SH-032 | 3D 1 | 8 s | 1–192 | — |
| SH-033 | 3D 1 | 7 s | 1–168 | — |
| SH-034 | 3D 1 | 8 s | 1–192 | **OUT 1**: f192 fog → eraser smudge |
| SH-050 | 3D 2 | 8 s | 1–192 | **IN 2**: f1 matches 2D SH-049 |
| SH-051 | 3D 2 | 12 s | 1–288 | — (2D counter area kept clear) |
| SH-052 | 3D 2 | 10 s | 1–240 | **OUT 2**: f240 shard reflection |
| SH-064 | 3D 3 | 8 s | 1–192 | **IN 3**: f1 side-window glass |
| SH-065 | 3D 3 | 8 s | 1–192 | — |
| SH-066 | 3D 3 | 4 s | 1–96 | — (ends on white) |
| SH-067 | 3D 3 | 10 s | 1–240 | **OUT 3**: f240 cracked glass |
| SH-083 | 3D 4 | 7 s | 1–168 | **IN 4**: f1 overexposed glare |
| SH-084 | 3D 4 | 6 s | 1–144 | — (date area kept clear) |
| SH-085 | 3D 4 | 9 s | 1–216 | — |
| SH-086 | 3D 4 | 8 s | 1–192 | **OUT 4**: f192 CRT reflection |

**Total: 3D frames = 2,880 (120 s).** On the laptop GPU, budget roughly 2–8 s per frame at 1080p and 32 samples in EEVEE, which is 1.5–6.5 hours of final rendering. Always test stills first.

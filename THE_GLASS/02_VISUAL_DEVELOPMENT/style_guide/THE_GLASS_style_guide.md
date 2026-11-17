# THE GLASS: Visual style guide v0.1

Status: **working draft**. It is based on prototype v001 (SH-028 → SH-031). It has not been approved.

## 1. Two worlds, one doorway

| | 🟦 2D, the narrated story (~11 min) | 🟥 3D, cinematic reconstructions (4 × 30 s) |
|---|---|---|
| Role | Explains, connects and keeps the timeline readable | Puts the viewer inside four turning points |
| Look | Editorial paper and print. Layered cutouts with 2.5D parallax | Stylised low-poly sets with grounded, practical lighting |
| Camera | Eased push-ins, map moves and inserts. Few whip pans | Physical crane, dolly and locked-off moves, 24–85 mm |
| Doorway | **Glass.** Every switch goes through a tear, crack, reflection or breath on glass ||

## 2. Palette

`color_palette/THE_GLASS_palette.png`

| Token | Hex | Use |
|---|---|---|
| Night navy | `#17212B` | Base shadow and desk; the world is cold |
| Slate | `#556774` | Secondary surfaces, walls, map land |
| Ivory | `#E9E6DE` | Paper, documents, title type |
| Amber | `#C78B55` | The **only** warm accent: lamp light, the lit window, the cash room |
| Oxide red | `#A95149` | Stamps, warnings, "UNPROVEN" labels. Never decorative |
| Ink | `#262C34` | Handwriting and line art |
| Glass green | `#78A08C` | Tint of the armoured glass, crack transitions |
| Málaga sun | `#E8C27A` (proposed) | Used **only** in 🎬 4, to make the contrast obvious |

Rule: amber means *money / the target*. Cool blue means *the outside world / the police / the night*.

## 3. Typography (all fonts are licensed for free use, see `03_2D_ASSETS/typography/`)

| Role | Font | Notes |
|---|---|---|
| Handwriting (Toska's notebook) | **Caveat** 400/600 (OFL) | Notebook pages only |
| Stamps and evidence labels | **Special Elite** (Apache 2.0) | CALLED OFF, ARRESTED, UNPROVEN |
| Dates, numbers, cards | **Oswald** 400–600 (OFL) | Calendar cards, 113 counter, 57M / 181 YEARS |
| Titles and lower thirds | **EB Garamond** 400/500 (OFL) | Chapter titles, names, memorial text |

Use at most two families per frame. Never let AI generate text in final frames.

## 4. 2D rules

- Build every shot from reusable layers: desk/background, paper, line art, cutout props, light pool, grain and vignette.
- Paper has fine grain and a faint 44 px grid. Desk texture should be barely visible (the prototype v001 was revised down after it looked blotchy).
- People are **silhouettes or cutouts without faces**. Names appear as typographic cards (A09).
- Motion: eased, deliberate and slow. One main movement per shot (camera *or* object). Nothing bounces.
- Every frame has a vignette (about 38 % at the corners) and a light pool from one direction.

## 5. 3D rules (laptop-friendly)

- EEVEE, 16 samples for previews, low-poly blockouts, procedural materials only and no external textures.
- Light: one warm practical light (window or lamp) against a cold key. The silhouette always gets a cold rim light, or it disappears against dark walls (this was found in prototype v001).
- Glass: on the laptop, use alpha-blended laminated layers, not raytraced transmission. Software EEVEE showed the window as black when transmission was used.
- Figures: anonymous, hooded and faceless (M03b). Prototype v001 uses a crude **blockout** figure that still needs proper modelling.

## 6. Signature transition (built in prototype v001)

`IN 1` (SH-030 → SH-031). Timings are from the prototype:

1. 17.2–18.4 s: the pen tears the paper across the WINDOW rectangle.
2. 18.35–19.0 s: the tear becomes a branching glass crack and a green glass tint fades up.
3. 19.0–20.0 s: about 42 Voronoi shards fly toward the camera and fade, revealing **frame 1 of the 3D render**. That frame is held under the shards, so the cut is invisible.
4. Sound: paper tear → glass ring → tinkle → whoosh → the 3D wind bed.

Every other transition reuses this template. Only the trigger changes (breath, glare, screen reflection), and the intensity drops for 🎬 3 (Klungland).

## 7. Things to avoid (from the brief, enforced)

PowerPoint-style templates, childlike cartoons, elastic motion, random transitions, AI-generated text, fabricated "evidence" that looks authentic, identifiable witnesses or relatives, weapon glamour shots, and any depiction of the moment Klungland was struck.

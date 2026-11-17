# Quality control: prototype v001 (03:30–03:57)

Reviewed by Claude, by inspecting rendered frames and contact sheets. **Not approved.** Only you can approve.

## Technical

| Check | Result |
|---|---|
| Resolution / frame rate | 1280×720, 24 fps. The 3D part is rendered at 960×540 and upscaled, which is preview quality |
| Duration | 27.0 s = 480 frames of 2D + 168 frames of 3D |
| Missing frames | None. Every frame is counted before encoding |
| Audio | 48 kHz stereo, about −18.5 LUFS integrated, **TEMP** |
| Files open | Encoded with ffmpeg and probed with ffprobe |

## Visual, 2D (SH-028 → SH-030)

| Item | Status | Notes |
|---|---|---|
| Layered notebook, pen and lamp pool | ✅ | Reads as editorial paper animation, not a template |
| Calendar card + **CALLED OFF** stamp | ✅ fixed | v0 had the stamp covering "FEB"; it now sits on the card edge |
| Desk texture | ✅ fixed | v0 looked blotchy; contrast reduced |
| Tear → crack → shards transition | ✅ | Shards reveal the real 3D frame 1, so the match is exact |
| Remaining weakness | ⚠️ | The pen is a flat cutout with no hand. The shard edges are hard (Voronoi) and could use a bright bevel and edge glints |

## Visual, 3D (SH-031)

| Item | Status | Notes |
|---|---|---|
| Camera crane, roof → over the shoulder | ✅ | Smooth Bezier ease; ends with the lit window over the figure's shoulder |
| Lit window, warm against cold | ✅ fixed | Transmission glass rendered black, so the window is now alpha-blended laminated layers |
| Silhouette visibility | ✅ fixed | It was invisible against the dark wall; a cold rim light was added |
| Figure quality | ❌ **blockout only** | Beveled boxes. Needs a proper low-poly hooded figure (M03b) before any final render |
| Frost on cobbles | ⚠️ | Still reads a little like patchy camouflage from high angles |
| Room behind glass | ⚠️ | Very plain. Add shelving and cash-room props (M06) for SH-032 |
| Render quality | ⚠️ | EEVEE at 16 samples with software GL shows slight grain. Expect a cleaner result on the laptop GPU |

## Historical

| Item | Status |
|---|---|
| Feb 2004 attempt shown as **called off**, not "the glass won" | ✅ corrected (S04, S05) |
| 3D 1 labelled as a reconstruction with dramatised light and weather | ✅ in the storyboard (source class column) |
| No weapons, no faces, no identifiable staff | ✅ |
| "Third attempt" wording avoided in VO | ✅ VO says "not the first time" |

## Audio

The TEMP VO is a robotic TTS (Festival) and must be replaced. The SFX (pencil, stamp, tear, glass ring, wind) are synthesised placeholders and are fine for timing. A sound designer should replace them.

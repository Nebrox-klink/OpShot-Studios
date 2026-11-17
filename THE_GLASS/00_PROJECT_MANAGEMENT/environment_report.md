# Environment report: 17 Nov 2026 (Phase A)

## Where this work ran

| Environment | Reachable? | What ran there |
|---|---|---|
| **Cloud container** (Linux, 4 vCPU, 15 GB RAM, no GPU) | ✅ | Everything in this delivery |
| **Your Lenovo Yoga Pro** (Windows, Blender, DaVinci Resolve) | ❌ **Not connected** | Nothing |

`list_computer_folders` returned **no folders**. Your laptop is not shared with this session through Remote Control, so I could not open, inspect or control Blender, Resolve, Krita or Inkscape on it. I made **no** GUI or desktop operations, and **no** claim in this delivery assumes that I did.

**To give a later session access to your laptop:** in the Claude desktop app on the laptop, go to *Settings → Claude Code → Remote Control* and add the `THE_GLASS` folder. That page may not offer folder sharing to every account yet. If it doesn't, run the scripts below yourself; each one starts with exact run instructions.

## Tools verified in the container

| Tool | Version | Verified how |
|---|---|---|
| Python | 3.13.18 (+ a 3.11 venv for bpy) | ran |
| **Blender (bpy module)** | **5.0.1** | Built a scene and rendered stills and 168 frames with EEVEE (software GL / llvmpipe) and Cycles |
| FFmpeg | 6.1.1 | Encodes, mux, concat, drawtext |
| Pillow / NumPy / openpyxl | 12.3 / 2.5 / 3.1.5 | 2D renderer, storyboard builder |
| Festival TTS + `cmu_us_slt_arctic_hts` | apt | TEMP VO only |
| Fonts | Caveat, Oswald, EB Garamond (OFL), Special Elite (Apache-2.0) | Loaded in Pillow from `.woff` |

**Blocked by the network policy:** github.com raw files, huggingface.co, en.wikipedia.org, snl.no, lokalhistoriewiki.no and klikk.no. As a result:
- The historical fact-check was done through **search-result summaries**, not full-text reading. `source_log.csv` records the access level for every source.
- No neural TTS voice could be downloaded. Festival is the only offline voice.

## Performance (measured)

| Job | Setting | Time |
|---|---|---|
| SH-031 EEVEE still, 960×540 | 8 samples | ~4.5 s/frame (noisy) |
| SH-031 EEVEE still, 1280×720 | 16 samples | ~35 s/frame |
| **SH-031 EEVEE animation, 960×540** | **16 samples** | **~23 s/frame, 168 frames ≈ 65 min** |
| 2D notebook (Pillow), 1280×720 | 480 frames | ~3 min total |

**What this means for the laptop:** EEVEE on the integrated Intel GPU (Arc/Iris Xe class) should be *much* faster than software rendering here. Expect roughly 1–5 s per frame at 720p for this blockout scene, but verify it with one still first. For 1080p finals, keep EEVEE at 16–32 samples, keep raytracing off, and use alpha-blended glass (see the style guide, §5).

## Lessons from Phase A that change the pipeline
1. **Transmission glass renders black** in software EEVEE. Use the alpha-blended laminated layers (`M02_glass_laminated`).
2. **Dark silhouettes vanish** against dark walls. A cold rim light is now part of the scene template.
3. In the bpy helper, `transform_apply()` applies location and rotation by default, which threw the figure parts off-screen. It is fixed and documented in the script.

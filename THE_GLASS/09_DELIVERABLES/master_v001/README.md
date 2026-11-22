# Final master v001 (1080p, pre-clearance) — superseded by v002

> **v001 contains a rule break:** at 7:06–7:20, motion clip M_1601 (16.1) pans onto a readable shop sign. **v002** (`../master_v002/`) uses the 16.1 still instead; everything else is identical. The animatics v008e–v008h have the same issue.

**File:** `THE_GLASS_MASTER_v001_1080p_PRE-CLEARANCE.mp4`. It is too large for git, so it is ignored here; rebuild it with the command below. It is technically finished but **not cleared for publication** (see "Before release").

## What it is

- **The edit:** the same as motion animatic v008h, with 8 still redos and 43 motion clips; 11:44 of film, followed by 5 draft credit cards of 7 s each.
- **Video:**
  - 1920×1080, 24 fps, H.264.
  - Intermediates at CRF 14.
  - Stills are taken from the 2752×1536 final JPGs. Camera moves are rendered at 2× resolution, so they don't jitter.
- **Motion clips:** generated at 720p and upscaled to 1080p in ffmpeg (Lanczos plus light unsharp). They are slightly softer than the stills. A native 1080p regeneration (Seedance `std`, about 22.5 credits per clip, about 970 for all 43) was not done, because the balance is about 148 credits.
- **Audio:** the final mix `07_AUDIO/mix_v008b/THE_GLASS_mix_v008b.flac` (mono, 44.1 kHz), encoded as AAC; the encoder delivers about 156 kb/s for mono. It measures −17.3 LUFS integrated in the master. The credits run in silence.
- **Text:** all on-screen text (cards, lower-thirds, the 113 counter, captions) is drawn at 1080p. Its size scales from the 720p layout.

## Rebuild

From `THE_GLASS/`:

```
RES=1080 OUT_DIR=09_DELIVERABLES/master_v001 NAME=THE_GLASS_MASTER_v001_1080p_PRE-CLEARANCE.mp4 \
CLIP_CRF=14 AUDIO_BR=320k CREDITS=09_DELIVERABLES/master_v001/credits_DRAFT_v001.txt \
python3 -I 09_DELIVERABLES/tools/build_stills_animatic.py .
```

It takes about 15–25 minutes on 4 cores. The per-shot intermediates are written to `clips/`, which is ignored.

## Before release (open; the producer decides)

1. **Credits:** `credits_DRAFT_v001.txt` is a draft. Check the wording, the sources and whether to add a producer name.
2. **Licences:** confirm that the Higgsfield and ElevenLabs plan terms allow publishing and monetising the generated images, clips, voice, music and sound effects.
3. **Lawyer:** a Norwegian media lawyer reviews L8 (image rights), L13 (quotes) and this cut.
4. **Klungland family:** the letter (`01_SCRIPT_STORYBOARD/phase4/`) is sent by the producer.
5. **Facts to confirm in *Dødsranet*:** F20, F60, F08 and F16.
6. **Platform loudness:** YouTube normalises to about −14 LUFS. −16 is fine as delivered; no change is needed.
7. **Platform AI disclosure:** tick YouTube's AI-disclosure box at upload. The film already opens with a disclosure card.
8. **Publication only with the producer's explicit approval.**

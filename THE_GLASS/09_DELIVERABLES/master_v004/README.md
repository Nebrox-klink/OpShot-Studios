# Master v004: THE NOKAS ROBBERY (1080p, pre-clearance), current

Changes from v003:
1. **Title:** the on-screen title is now **THE NOKAS ROBBERY** (was THE GLASS), in the title card and the first credit card (`credits_DRAFT_v002.txt`). File and folder names in the project still say THE_GLASS.
2. **Scene 17 tail halved:** the pause after "Arne Sigve Klungland was killed there. He was fifty-three." was about 25 s, because scene 17 kept its full 50 s slot. It now follows the same rule as other scenes (half the remaining slot), giving about 12.7 s. The 6 s white silence at 08:17, before that line, is unchanged. The film is now 11:31 (was 11:44); with credits, 12:07.
3. **Mix:** `07_AUDIO/mix_v008d/THE_GLASS_mix_v008d.flac`, at −16.0 LUFS integrated and −1.8 dBTP.
4. **Subtitles (English):** see `subtitles/`.

## Files

| File | What | In git |
|---|---|---|
| `THE_NOKAS_ROBBERY_MASTER_v004_1080p_PRE-CLEARANCE.mp4` | Clean master, no subtitles | no (rebuild below) |
| `THE_NOKAS_ROBBERY_v004_1080p_SUBTITLED_share.mp4` | Burned-in subtitles, 3.6 Mb/s share copy | no |
| `subtitles/THE_NOKAS_ROBBERY_v004_en.srt` | Toggleable captions (upload to YouTube with the clean master) | yes |
| `subtitles/THE_NOKAS_ROBBERY_v004_en.ass` | Netflix-style styling used for burn-in | yes |

## Subtitles

- **Style:** Netflix-style: Inter Medium, white, a soft shadow and a thin dark outline, no box, bottom centre.
- **Layout:** at most 42 characters per line and 2 lines; 0.83–7 s per cue; at most 20 characters per second; a 2-frame gap between cues.
- **Line breaks:** at grammatical boundaries.
- **On-screen text:** cues that overlap a lower-third or the memorial caption are raised above it.
- **Text:** exactly the narration (from the voice prompts, with names restored); English, narration only.
- **Timing:** each line is placed where the mix places it, then spread over the speech detected in its audio, with edges snapped to pauses.
- **Tool:** `09_DELIVERABLES/tools/make_subtitles.py` (no cost, offline).

## Rebuild

From `THE_GLASS/`:

```
RES=1080 OUT_DIR=09_DELIVERABLES/master_v004 NAME=THE_NOKAS_ROBBERY_MASTER_v004_1080p_PRE-CLEARANCE.mp4 CLIP_CRF=14 AUDIO_BR=320k \
  CREDITS=09_DELIVERABLES/master_v004/credits_DRAFT_v002.txt python3 -I 09_DELIVERABLES/tools/build_stills_animatic.py .
python3 -I 09_DELIVERABLES/tools/make_subtitles.py . 09_DELIVERABLES/master_v004/clips 09_DELIVERABLES/master_v004/subtitles/THE_NOKAS_ROBBERY_v004_en
```

Burn-in: `ffmpeg -i <clean master> -vf "ass=subtitles/THE_NOKAS_ROBBERY_v004_en.ass" -c:v libx264 -crf 16 -preset slow -c:a copy <out>.mp4`

It is **not cleared for publication**. The checklist in `../master_v001/README.md` still applies.

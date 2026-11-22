# Master v005: THE NOKAS ROBBERY, tight timing (1080p, pre-clearance), current

v005 answers the feedback that "the pauses are very long, and the voice is flat and monotone":
- **Pauses:** fixed with tight timing (v009).
  - Pauses inside a line are at most 0.8 s.
  - About 1.5 s separates scenes.
  - The white silence at 08:17 is 3 s (was 6 s).
  - The cold open, the 113 counter and the ending are unchanged.
  - The rule lives in `09_DELIVERABLES/tools/timing.py`, shared by the mix, the picture and the subtitles.
- **Voice:** unchanged (the producer's choice for now).

The film is **9:54** (v004 was 11:31); with the draft credits, 10:30. The mix is `07_AUDIO/mix_v009/THE_GLASS_mix_v009.flac`, at −15.9 LUFS and −1.8 dBTP. The title is THE NOKAS ROBBERY, and the credits are `../master_v004/credits_DRAFT_v002.txt`.

| File | What | In git |
|---|---|---|
| `THE_NOKAS_ROBBERY_MASTER_v005_1080p_PRE-CLEARANCE.mp4` | Clean master | no (rebuild below) |
| `THE_NOKAS_ROBBERY_v005_1080p_SUBTITLED_share.mp4` | Burned-in Netflix-style subtitles, 3.6 Mb/s | no |
| `subtitles/THE_NOKAS_ROBBERY_v005_en.srt` / `.ass` | English subtitles: 187 cues, at most 20 characters per second | yes |
| `youtube_description_v002.txt` | The YouTube description with chapter times for v005 | yes |

**Rebuild** (from `THE_GLASS/`):

```
RES=1080 OUT_DIR=09_DELIVERABLES/master_v005 NAME=THE_NOKAS_ROBBERY_MASTER_v005_1080p_PRE-CLEARANCE.mp4 CLIP_CRF=14 AUDIO_BR=320k \
  CREDITS=09_DELIVERABLES/master_v004/credits_DRAFT_v002.txt python3 -I 09_DELIVERABLES/tools/build_stills_animatic.py .
python3 -I 09_DELIVERABLES/tools/make_subtitles.py . 09_DELIVERABLES/master_v005/clips 09_DELIVERABLES/master_v005/subtitles/THE_NOKAS_ROBBERY_v005_en
```

It is **not cleared for publication**. The checklist in `../master_v001/README.md` still applies.

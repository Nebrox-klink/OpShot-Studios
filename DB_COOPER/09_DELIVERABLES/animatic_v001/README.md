# D.B. Cooper rough animatic v001 (scenes 1–10, 3:53)

Built with `../tools/build_animatic.py . OUT.mp4 [scenes]`. It is free: local ffmpeg only.

- **Picture:** the 42 approved round-1 stills plus 5 reused style references, with a slow push, pull or pan on each shot and 0.35 s fades.
- **Cards:** the film title, and CLUE 1–2 (the builder can also make CLUE 3–6).
- **Narration:** Brian v001 (S01, S03–S06, S08–S10), using tight timing: 1.0 s lead-in and 0.5 s tail per scene. Video and audio are both 233.5 s.
- **Not in yet:**
  - Scene 7 narration (14 s placeholder with an on-screen note).
  - Cooper's line in scene 4 ("Miss, you'd better look at that note…").
  - Music, sound effects and subtitles.
- **Shot timing:** `DB_COOPER_animatic_v001_S01-S10_shots.txt` lists each shot's start time.

## v002 and v003
- **v002:** K01 (the open rear stairs) as motion at shots 102 and 704.
- **v003:** adds K03 (104), K04 (401), K05 (502) and K06 (801). Same timing and length as v001/v002 (233.5 s). Cards now draw over motion clips too. K07 (1101) and K08 (1301) are wired in and appear once scenes 11 and 13 have narration. K02 (103) is still pending.
- **v004:** adds K02 (103). Shots 102, 103, 104, 401, 502, 704 and 801 are now motion clips. Same length, 233.5 s.
- **v005 (FULL, scenes 1–23, 9:49):** all narration by Brian, all 8 Kling motion clips (K07 under CLUE 3, K08 under CLUE 5). The 16 round-2 shots (scenes 15–23) are a dimmed case board with a "still pending (round 2)" label. Not in yet: Cooper's line, music, sound effects, subtitles. Video and audio are both 588.7 s.
- **v006 (FULL, 9:53):** all 65 shots are real images (round 2 is done; no placeholders left). Cooper's line (Callum, intercom filter) plays 0.4 s after Brian's "He leans over." in scene 4, over shot 403, where he is seen from behind with no mouth visible. Tight pacing kept, as the producer decided. Not in yet: music, sound effects, subtitles. Video and audio are both 593.5 s.
- **v007 (SOUND, 9:53):** v006 picture with the full mix (`tools/mix_sound_v001.py`):
  - Brian, Cooper's line, music M1–M5 and 17 sound effects.
  - The bed is ducked 9 dB and one-shots 4 dB under the voice.
  - Loudness-normalised to −16 LUFS. The measured result is −16.6 LUFS, LRA 3.4.
  - The narration lines up with v006 to within 1 ms at five check points.
  - The mix is also saved as `07_AUDIO/mix_v001/DB_COOPER_mix_v001.flac`.
  - **Subtitles are not burned in:** they are a separate file for YouTube, `../subtitles_v001/DB_COOPER_en.srt`.
  - Not checked by ear yet.

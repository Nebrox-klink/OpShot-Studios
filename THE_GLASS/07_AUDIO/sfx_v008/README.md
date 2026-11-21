# Sound effects and music, v008

**Sound effects:** ElevenLabs `eleven_text_to_sound_v2`, flow "THE GLASS sound effects v008" (`h3bZMpLshOq3Ow4Rppt6`).
- **Pass 1 (39 cues, about 663 credits):** generated without a set duration, so most came back 0.5–2 seconds long.
  - Ten were kept: X05 bell, X07 chess piece, X10 muffled trolley, X12 organ, X17 coach bus, X29 ram on the vault gate, X38 shutter, X39 handle, X41 modem, X43 memorial.
  - The other takes I downloaded are kept in `pass1_too_short/` for the record.
  - The rest of pass 1 was not downloaded.
- **Pass 2 (25 cues, R01–R45, about 351 credits):** generated with explicit `duration_seconds`. Ambiences are 3–6 second seamless loops (`loop: true`) that the mix repeats.
- **Lesson for future work:** always set `duration_seconds` on sound effects. Sound effects cost about 3.3 credits per second; the estimate tool quotes about 10 per second, which is higher than what is charged.

**Music:** Higgsfield `elevenlabs_music_v2_5`, instrumental, about 44 credits. The files are in `07_AUDIO/music_v008/`.
- M1, robbers' drone: 120 s
- M2, Klungland's piano theme: 75 s
- M3, title and closing notes: 20 s
- M4, hunt pulse: 60 s
- M5, city dawn pad: 50 s

**Mix:** `09_DELIVERABLES/tools/mix_sound_v008.py`.
- The cue sheet is in the script: each cue has a scene, a start time within the scene, a gain and fades.
- Music and ambience are lowered by 9 dB wherever the narrator speaks; one-shot effects by 4 dB.
- 08:17 is forced to total silence for 6 seconds.
- The mix is loudness-normalised to about −16 LUFS.
- **Output:** `07_AUDIO/mix_v008/THE_GLASS_mix_v008.flac` and `09_DELIVERABLES/animatic_atlas_v008/THE_GLASS_animatic_atlas_sound_v008.mp4`.

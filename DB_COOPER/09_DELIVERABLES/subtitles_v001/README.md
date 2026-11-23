# English subtitles v001

- **`DB_COOPER_en.srt`:** upload this to YouTube (Subtitles → Add language → English → Upload file → With timing). 212 cues, timed to `DB_COOPER_animatic_v007_SOUND.mp4`. Cooper's line is in italics.
- **`DB_COOPER_en.ass`:** the same cues with styling, for an optional burned-in version. Not used: the producer wants subtitles as a separate file.
- **Made with** `../tools/make_subtitles.py . OUT_BASENAME`.
  - Text: Brian's narration prompts with the direction tags removed.
  - Timing: the same timeline as the animatic and the mix. Within each scene, cues are spread over the detected speech by character count and snapped to pauses.
  - Rules: at most 42 characters per line and 2 lines per cue; 0.83–7 s per cue; a 2-frame gap between cues.
  - Readability: 5 cues are slightly over 20 characters a second (max 22.1).
- **If any scene's narration is re-recorded or retimed, regenerate this file.**
- **No AI-disclosure card in the video**, as the producer decided. YouTube's "altered or synthetic content" setting at upload is a separate step.

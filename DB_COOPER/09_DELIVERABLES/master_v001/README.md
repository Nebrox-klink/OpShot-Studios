# D.B. Cooper master v001 (1080p)

- **File:** `DB_COOPER_master_v001_1080p.mp4`. 1920×1080, 25 fps, H.264 at CRF 16, AAC 320 kb/s at 48 kHz. 9:53 (593.5 s), about 443 MB.
- **Not in git:** the file is over GitHub's 100 MB limit, so `.gitignore` keeps it out, as was done for the NOKAS master. The producer was sent a copy on 23 Nov. To rebuild it, you also need the gitignored 2K stills (`02_VISUAL/shot_list_v001/stills/`):
  1. `DBC_W=1920 DBC_H=1080 DBC_CRF=16 python3 -I tools/build_animatic.py .. OUT.mp4 1,2,...,23`
  2. Mux in `07_AUDIO/mix_v001/DB_COOPER_mix_v001.flac`.
- **Picture:** the same cut as animatic v006/v007. The shot timing is identical (`DB_COOPER_master_v001_shots.txt`). It is rendered from the 2K stills, and the title, clue-card and placeholder text is scaled for 1080p.
- **Sound:** mix v001, approved by the producer on 23 Nov.
- **Subtitles:** a separate file, `../subtitles_v001/DB_COOPER_en.srt`. Nothing is burned in.
- **No AI-disclosure card in the video** (the producer's decision). Set YouTube's "altered or synthetic content" option at upload if it applies.
- **Kling clips:** the producer confirmed a paid Kling plan, which covers commercial use.
- **Before publishing:**
  - final watch-through;
  - choose the title and thumbnail (`../thumbnails_v001/`);
  - description and sources (the fact ledger has them).

# Atlas narration, script v008

- **Voice:** Atlas – Deep, Gravelly Narrator (`3YzGaTGef0x5PLEK9yGq`). **Model:** eleven_v4. One take per chunk.
- **Cost:** 7,785 credits, 1 per character, generated on 21 Nov 2026. ElevenLabs flow: "THE GLASS narration v008 (Atlas)", `LI8Vi1N6dZJFH2qcaETs`.
- **Prompts:** `atlas_prompts_v008.json` (built by `09_DELIVERABLES/tools/atlas_prompts.py`). Names are written in IPA; Kloongland and Shooman were confirmed by the producer.
- **Files:**
  - `S01.mp3` … `S24.mp3`: one chunk per scene. Scene 17 is split into `S17a.mp3` and `S17b.mp3` around the 6-second white silence.
  - `pilot_*.mp3`: the pilot takes. They are the same generations as `S02.mp3`, `S13.mp3` and `S17b.mp3`.
  - `THE_GLASS_narration_atlas_v008_full.flac`: the full track laid out on the scene slots, starting after the 4-second disclosure card. 13:05.
- **Rebuild the timeline and animatic:**
  ```
  python -I 09_DELIVERABLES/tools/build_animatic_audio.py SCRIPT.md MODELS_DIR OUT_DIR atlas:THE_GLASS/07_AUDIO/atlas_v008
  ```

# THE GLASS: handoff and production playbook

*Last updated 21 Nov 2026. Branch `claude/nokas-robbery-script-vwal6c`, repo `nebrox-klink/opshot-studios`.*

This file is the single source of truth for continuing THE GLASS and for making future videos with the same pipeline. Read this first.

---

## 1. Project in one paragraph

THE GLASS is an animated documentary of about 12 minutes, in English, about the NOKAS robbery (Stavanger, 5 April 2004). It is built between two funerals:
- the robbers wore white armbands for Toska's friend William Ellingsen;
- a year later, Toska was arrested while reading about the memorial for police officer Arne Sigve Klungland.

The dramatic question changes from **"Will the plan work?"** to **"Who pays for it?"**. Core line: *"Grief built the plan, and the plan made grief."* Closing line: *"…was never on his board."*

## 2. Standing rules (the producer's rules; never break them)

**Spending and permissions:**
- No paid generation, credit purchase or billable compute without explicit approval. Account access is not permission to spend.
- Explicit approval is also needed before:
  - deleting files;
  - installing unverified apps;
  - uploading confidential material;
  - publishing;
  - using third-party copyrighted material.

**Honesty and file handling:**
- Never fabricate completion. Never call a rough cut publication-ready.
- Keep originals and use versioned copies (v008, v008b…). Do not delete; move superseded files aside.
- Mark uncertain facts. Never fill a gap from memory.

**Ethics and portrayal:**
- **Klungland:** dignity, no gore, no invented words, never shown in the vehicle, no likeness without the family's consent.
- **No glorifying the robbers:** faceless silhouettes, no hero poses or slow motion, no thrill music. Toska is only ever seen from behind.
- **Generation hard limits:**
  - no lip sync;
  - no hands doing precise work;
  - no crowds in motion;
  - no glass breaking in motion;
  - no fire spreading;
  - no text inside generated images (all text is added in the edit).

**Process:**
- Every still is approved before anything moves.
- Every generated clip is checked at its start, middle and end; drop a tier on any warping; at most two attempts per shot.
- Replies to the producer are always in English, even when they write in Norwegian.

## 3. Status (what is done)

| Stage | Status | Where |
|---|---|---|
| Phase 1 research | Done. 65 facts (F01–F65), 17 sources | `02_RESEARCH/THE_GLASS_fact_ledger_v002.csv`, `…source_register_v002.csv`, `…phase1_research_dossier_v001.md` |
| Phase 2 story design | Approved | `01_SCRIPT_STORYBOARD/phase2/THE_GLASS_phase2_story_design_v001.md` |
| Phase 3 script | Approved | `01_SCRIPT_STORYBOARD/revised/THE_GLASS_script_v007_phase3.md` |
| Phase 4 review gates | Approved; edits applied in v008 | `01_SCRIPT_STORYBOARD/phase4/…review_gates_v001.md`, family letter draft, screening kit |
| **Script (current)** | **v008**: 24 scenes, every line tagged with a fact ID or [FRAMING], about 7,400 characters | `01_SCRIPT_STORYBOARD/revised/THE_GLASS_script_v008.md` |
| Test screening | **Skipped by the producer** | — |
| Atlas narration | Done (25 chunks) | `07_AUDIO/atlas_v008/` |
| Music | Done (5 cues) | `07_AUDIO/music_v008/` |
| Sound effects | Done (35 usable) | `07_AUDIO/sfx_v008/` |
| Mix (current) | **v008b**: tightened timing, 11:44 | `07_AUDIO/mix_v008b/THE_GLASS_mix_v008b.flac` |
| Style references | Approved | `02_VISUAL_DEVELOPMENT/style_refs_v001/` |
| Shot stills | 65 finals (63 plus 2 officer stills) | `02_VISUAL_DEVELOPMENT/shot_stills_v001/final_jpg/` |
| Motion | 18 Seedance clips, all passed the check | `06_AI_VIDEO/motion_v001/clips/` |
| **Latest cut** | **Motion animatic v008e, 11:44** (six still redos plus six pilot motion clips) | `09_DELIVERABLES/animatic_motion_v008e/THE_GLASS_motion_animatic_v008e.mp4` |

**Abandoned:** the four Blender 3D sequences (dropped by the producer). Their files remain in `05_BLENDER/`, untouched.

## 4. Open items (next steps)

1. **Producer review of the motion animatic.** Expect notes on timing, sound and stills.
2. **Still redos:**
   - **Done (22 Nov):** 11.1, 12.1, 12.2, 16.2, 18.3 and 22.4. Details are in the shot stills README (v002 redos); 12.2 also got a new motion clip, M_12022.
   - **Still open (optional, 2 credits each):** 7.2, 23.1.
3. **More motion (pilot 2 done: 1.2, 6.1, 10.2, 14.1, 16.1, 21.2).** The suggested next set, 12.5 credits each: 2.3, 3.1, 7.1, 8.1, 9.1, 9.3, 17.2, 18.1, 19.1, 22.3, then 4.1, 4.2, 8.2, 9.2, 15.1, 15.2, 17.1, 20.2, 23.1. Keep still: glass breaking, the rifle and hammer shots, the officer stills (9.4, 19.3), the CCTV shot (12.1), walking figures.
3b. **Klungland:** the producer chose anonymous officer stills (9.4 and 19.3) over a portrait. The captions are "Arne Sigve Klungland" and "In memory of Arne Sigve Klungland · 1950 – 2004". If a reference photo is provided later, redo 9.4 / 19.3 to resemble it, but only with the family's consent.
4. **Family letter** (`01_SCRIPT_STORYBOARD/phase4/THE_GLASS_klungland_family_letter_DRAFT_v001.md`): the producer sends it. Have a native speaker check the Norwegian first.
5. **Before publication:**
   - a Norwegian media lawyer reviews L8 (image rights), L13 (quotes) and the final cut;
   - final credits (NRK, Aftenblad, Aftenposten, Wikipedia, SNL, music and sound licences);
   - tick YouTube's AI-disclosure box;
   - **publication needs explicit approval.**
6. **Final master:** the animatics are 720p. For a release, upscale the stills or regenerate at 4k, and consider Seedance `std` mode at 1080p (22.5+ credits per clip).
7. **Medium-confidence facts to confirm in *Dødsranet*:** F20 (15 seconds), F60 (chess), F08 (15 March), F16 (silence).

## 5. Accounts, IDs and balances (21 Nov 2026)

**ElevenLabs** (Starter plan, 40,000 credits a month): about 5,800 left this month.
- **Narrator:** Atlas – Deep, Gravelly Narrator, voice `3YzGaTGef0x5PLEK9yGq`.
- **Model:** `eleven_v4`. Use tags like `[softly]` and `[pause]`; names go in IPA between slashes.
- **Flows:** narration `LI8Vi1N6dZJFH2qcaETs`; sound effects `h3bZMpLshOq3Ow4Rppt6`.
- **Pronunciations confirmed by the producer:**
  - Klungland /ˈkluːŋlænd/ ("Kloongland");
  - Schumann /ˈʃuːmən/ ("Shooman").
- **Other IPA in `09_DELIVERABLES/tools/atlas_prompts.py`:** Arne Sigve, Håland, Sørmarka, Nedre Dalgate, NOKAS, Stavanger, Sandnes.
- **Earlier voice candidates:**
  - Verdict `ZmqEPiBIr4itJeB29TyD`
  - Oliver `lo1O1Dz1Tu4FWVEPaxuT`
  - Leo `oJUpLOe3yEYTEIjO6ddh`
  - Philip `exurTFaGNF2gnRcPNH8I`
  - Imogen `jv41DhCf464zw0TI7I1w`
  - David `rSLmFOTRq9g87aTxSUr6`

**Higgsfield** (Plus plan): **about 415 credits left** (22 Nov, after the redos).

**Style reference job IDs** (pass them as `image_references`):

| Reference | Job ID |
|---|---|
| BG1 courtyard | `51586c50-8a26-4f88-83bd-bac68e376044` |
| BG2 counting room | `24d23986-fca7-451a-b2bb-03f602511b57` |
| BG3 cathedral square | `d691a1fb-90d8-4292-8224-e33c22ceafbb` |
| BG4 hotel street | `add729dd-cf38-4eec-8a6c-70c3174bec60` |
| CH1 Toska (back views) | `f90ae53d-c66f-4d10-bfc2-906fb4dfa3db` |
| CH2 robber silhouette | `6a11be37-5311-4589-8fe4-7d9f606c57c0` |

The job ID of every still and clip is in `shot_stills_v001/jobs.tsv` and `motion_v001/jobs.tsv`. Masters can be re-downloaded from the Higgsfield history.

**Free placeholder voice:** Kokoro-82M (kokoro-onnx 0.6.1).
- The models come from the kokoro-onnx GitHub release `model-files-v1.0` (sha256 in `07_AUDIO/placeholder_voice_kokoro/README.md`).
- Producer's choice: `bm_george`.
- The venv lives in the scratchpad and must be reinstalled in a new container: `pip install kokoro-onnx soundfile pillow`.

**Environment:** cloud env `env_01NSZbHuqXiJmxSdeebyCj8E`.
- Allowed hosts include the Higgsfield/CloudFront, ElevenLabs, Norwegian news, Lovdata, nb.no and MET hosts.
- Adding web.archive.org was rejected; don't re-ask.
- GitHub release assets download fine; huggingface.co is blocked.

## 6. The pipeline (reusable for future videos)

**Stage A, research → story → script → review**
1. **Research:** a fact ledger CSV with columns id, when, claim, sources, confidence, conflict; plus a source register. Read the sources rather than relying on memory, mark conflicts, and list the primary sources you couldn't reach.
2. **Story design:** a dramatic question (surface question → real question), an emotional core, a glorification test (G1–G6), an irony and surprise plan, a beat sheet linked by but/therefore, plants and payoffs.
3. **Script for the ear:** tag every line `[F##]` or `[FRAMING]`/`[DRAMATISED]`/`[CONTEXT]`. Format per scene: VISUAL with tiers / NARRATION / DIALOGUE / SOUND. Write a pronunciation guide. Check timing with `09_DELIVERABLES/tools/narration_timing.py` (about 14 characters per second).
4. **Review gates:** a legal and ethics checklist (Vær Varsom as the standard), a sensitivity pass, a family letter, a screening kit.

**Stage B, sound**
1. **Placeholder animatic (free):**
   `python -I 09_DELIVERABLES/tools/build_animatic_audio.py SCRIPT.md MODELS_DIR OUT_DIR bm_george 0.9`
2. **Narration:**
   - build per-scene prompts with `atlas_prompts.py`;
   - pilot 2–3 chunks containing the hard names, and have the producer approve them;
   - generate every chunk with `creative_generate_speech`, `generations_count: 1` (the default is 2, which doubles the cost);
   - split a scene where a long scripted silence falls (S17a/b).
3. **Music:** Higgsfield `elevenlabs_music_v2_5`, `force_instrumental`, about 8.7 credits per minute. Generate a few long cues and reuse them.
4. **Sound effects:** ElevenLabs `eleven_text_to_sound_v2`, created via `creative_add_flow_node` with **`duration_seconds` set** (otherwise it returns 0.5–2 s takes) and `loop: true` for ambiences.
   - Charged about 3.3 credits per second; the estimate tool over-quotes.
   - The concurrency limit makes ElevenLabs queue jobs automatically. Never resubmit.
5. **Mix:** `09_DELIVERABLES/tools/mix_sound_v008.py`.
   - The cue sheet is in the script: scene, start time in the scene, gain, fades.
   - Ducking: −9 dB on music and ambience, −4 dB on hits.
   - Forced silence where the script calls for it.
   - Loudness normalised to −16 LUFS.
   - **Timing rule v008b:** scene length = narration + half of the remaining slot. Scenes 1, 13, 17 and 24 keep their full slot.

**Stage C, pictures**
1. **Style references:** 4 master backgrounds and 2 character sheets. Use Nano Banana 2.1 (`nano_banana_2_1`) at 2k and 16:9 (2 credits each), with this style block:
   > "Painterly 2D gouache illustration for a serious animated documentary, graphic-novel lighting, visible brush strokes, muted palette, atmospheric haze, cinematic composition, not photorealistic; match the style of any reference images. No text, letters, numbers, signs or logos. No blood."
   Never use "photorealistic" or "8K".
2. **Shot stills:** `02_VISUAL_DEVELOPMENT/shot_stills_v001/make_shot_prompts.py`, with references from step 1.
   - Submit with `generate_image_batch`, **at most 8 jobs at once** (`next.py N` queues the next ones).
   - Download with `dl.sh`, review on labelled contact sheets, and redo anything that breaks a rule.
3. **Motion:** Seedance 2.0 (`seedance_2_0`), image-to-video, `start_image` = the still's job ID.
   - Settings: 5 s, 720p, `mode: fast`, `generate_audio: false`. 12.5 credits per clip.
   - Video allows **at most 6 jobs at once**.
   - Prompts: "Static camera. <one subtle motion>. Nothing else moves. Keep the painterly illustrated style exactly. No people, no text."
   - Check with `06_AI_VIDEO/motion_v001/dlm.sh` (frames at 0.2, 2.5 and 4.8 s).
4. **Animatic:** `python3 -I 09_DELIVERABLES/tools/build_stills_animatic.py THE_GLASS_ROOT`.
   - Shot order, durations, cards, lower-thirds, the 113 counter and the captions are set in its `PLAN` dict.
   - Motion clips are swapped in through its `MOTION` map; set `USE_MOTION=0` to use stills only.
   - It reads `mix_v008b` and writes to `animatic_motion_v008e`. Bump the output version before each new build.
   - Shrink the output with `crf 27` before committing; GitHub warns above 50 MB.

## 7. Lessons learned (do not repeat)

**Generation and spending:**
- ElevenLabs sound effects without `duration_seconds` come back 0.5–2 s long. About 660 credits were wasted this way.
- Leave generation counts at 1 unless takes are wanted; the defaults double the spend.
- Higgsfield rate limits: 8 image jobs and 6 video jobs at once. Submit in waves.
- Generated images drift American (police cars, fire escapes, semi trucks). Say "Norwegian, 2004, Volvo" explicitly.
- "Seen from behind" still gives profiles sometimes. Say "only the back of the head, no face, no profile, no ear". Character redos fixed 6.1 and 22.3.
- An action pose for a rifle reads as glorification. Ask for "rifle held low, static, ordinary".

**Files and the environment:**
- Keep file names identical to script shot numbers; a mismatch broke one render.
- Blender 5.3 EEVEE freezes SH-052 frames; portable 5.0.1 works (relevant only if 3D returns).
- The ElevenLabs connector needs `ToolSearch` again whenever it reconnects; poll with `creative_get_flow_run_status`.
- Download URLs expire after a few hours. Download as soon as jobs complete.

## 8. Key facts quick sheet (for script or visual decisions)

**The morning of 5 April 2004:**
- 08:01–08:02: sledgehammer and a 70 kg ram on the glass.
- 08:02:58: alarm registered by the police.
- 08:03: Toska fires first, then Schumann (AG3). 113 shots in total.
- 08:03–08:09: three women move 60 million kroner into the lift.
- 08:08:16: the first police car arrives (Håland and his partner, 12 rounds each).
- 08:08:39: the robbers are inside, six minutes behind plan.
- Inside: mostly 200-kroner notes; the barred vault gate was unlocked.
- 08:14: shoot-out on the square.
- 08:17: Klungland is killed (Kongsgata by the Maritim hotel or Klubbgata); a bus blocked his reversing.
- 08:20:15: the last car leaves. The cars are burned at Sørmarka.
- Later that day: six robbers sit in a flat on Nedre Dalgate.

**Evidence:** an earplug carrying Toska's DNA, and fires that failed to burn.

**Klungland:** aged 53 (1950–2004); 30 years in the police; dog handler, rescue leader, trainer of police students, driver of the pensioners' church-trip bus. He briefed the patrols that morning. Married in 1977; two children. Funeral 14 April 2004 in Stavanger Cathedral, about 600 officers.

**The arrest:** 5 April 2005 in Málaga, while Klungland's memorial was under way. The police had his email provider (postmaster.co.uk; address "omaha beach") slow down logins.

**Verdicts:** 13 men convicted. Supreme Court (29 June 2007): Toska **18 years**; Schumann 16 years' preventive detention. Schumann says the shot was a mistake; the court found it was aimed.

**Money:** 57.4 million kroner stolen; about 51 million never found. 32 NOKAS employees had late psychological effects ten years on.

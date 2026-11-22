# Atlas narration, tightened (v009 timing)

These are copies of `../atlas_v008/S*.mp3` in which every pause longer than 0.8 s is shortened to 0.8 s (with a 20 ms crossfade) and the chunk edges are trimmed. They were made because viewers found the pauses too long. The originals are unchanged.

- **Tool:** `09_DELIVERABLES/tools/tighten_narration.py SRC OUT 0.8`
- **Time maps:** `time_maps.json` maps old to new time per chunk. `timing.py` uses it to move sound cues onto the same words.
- **Saving:** 13.0 s inside the lines (522.2 s → 509.2 s). Most of the overall saving comes from the shorter scene gaps (see `timing.py`).
- **Use:** scenes 1, 13 and 24 keep the original audio, because their sound design is timed to it.

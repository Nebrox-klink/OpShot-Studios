# Final master v003 (1080p, pre-clearance): current

**File:** `THE_GLASS_MASTER_v003_1080p_PRE-CLEARANCE.mp4` (not in git; about 576 MB).

It is the v002 picture, stream-copied with no re-encode, with the audio replaced by **mix v008c**, normalised to **−16.0 LUFS** (true peak −1.6 dBTP after AAC). Everything else (specs, credits, the 16.1 still) is as in v002. v001's README has the pre-release checklist.

**Rebuild:** first build v002 (see `../master_v002/README.md`), then:

```
ffmpeg -i ../master_v002/video_only.mp4 -i ../../07_AUDIO/mix_v008c/THE_GLASS_mix_v008c.flac -map 0:v -map 1:a \
  -c:v copy -af apad -t 739.458 -c:a aac -b:a 320k -movflags +faststart THE_GLASS_MASTER_v003_1080p_PRE-CLEARANCE.mp4
```

For a future full rebuild, point `MIX` in `build_stills_animatic.py` at `mix_v008c`.

It is **not cleared for publication**.

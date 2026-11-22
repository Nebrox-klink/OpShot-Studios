# Mix v008c: loudness-corrected final mix

v008b, measured with ffmpeg `ebur128`, comes out at **−17.3 LUFS** integrated, not the −16 that was intended. v008c raises it to **−16.0 LUFS**. Its true peak is −1.8 dBTP and its LRA 9.4 LU (the dynamics are unchanged). v008b is untouched.

```
ffmpeg -i ../mix_v008b/THE_GLASS_mix_v008b.flac \
  -af "aresample=176400,volume=2.0dB,alimiter=limit=0.813:attack=3:release=60:level=disabled,aresample=44100:dither_method=triangular" \
  -sample_fmt s16 THE_GLASS_mix_v008c.flac
```

The limiter runs at 4× sample rate, so it also catches peaks between samples (true peaks), and only brushes the loudest moments. Two-pass `loudnorm` was rejected: it switched to dynamic mode, cut LRA to 7.5 and reached only −16.7.

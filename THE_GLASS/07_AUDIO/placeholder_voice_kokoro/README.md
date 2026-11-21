# Placeholder voice for the screening animatic (free, offline)

- **Engine:** kokoro-onnx 0.6.1 (MIT) from PyPI. **Model:** Kokoro-82M v1.0 (Apache-2.0 weights). Model files come from the kokoro-onnx GitHub release `model-files-v1.0`:
  - `kokoro-v1.0.onnx`: sha256 `7d5df8ecf7d4b1878015a32686053fd0eebe2bc377234608764cc0ef3636a6c5`
  - `voices-v1.0.bin`: sha256 `bca610b8308e8d99f32e6fe4197e7ec01679264efed0cac9140fe9c29f1fbf7d`
- **Runs on CPU,** in about 2 s per sentence. Nothing is sent to any service, and it costs $0.
- **Used for the animatic:** `am_michael` at speed 0.9. The samples here are the same cold-open lines in six male voices, so you can choose a different one.
- **This is a placeholder only.** The final narrator is still Atlas (ElevenLabs), which needs your separate approval.
- **Rebuild:**
  ```
  python -I 09_DELIVERABLES/tools/build_animatic_audio.py SCRIPT.md MODELS_DIR OUT_DIR [voice] [speed]
  ```

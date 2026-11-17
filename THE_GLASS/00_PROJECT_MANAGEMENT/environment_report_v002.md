# Environment report v002 (17 Nov 2026, from 17:00 Europe/Oslo)

Each item below was checked by running a command or tool call. Nothing in this report is assumed.

## Two execution environments

| | Cloud container (this Claude Code session) | Your laptop (reached through the **Higgsfield Blender bridge**) |
|---|---|---|
| How it's reached | Native shell | `bl_execute`, which runs Python inside your running Blender. That Python can start other processes |
| OS | Linux, 4 vCPU, 15 GB RAM, no GPU | **Windows 11** (10.0.26200) |
| CPU (reported) | — | 13th Gen Intel Core **i5**-13500H (the brief said i7) |
| RAM | 15 GB | 16.9 GB total, **only ~3.2 GB free** at 17:05 (Blender + Resolve + others open) |
| Disk free | ~28 GB of allowance | **341 GB** on C: |
| Blender | bpy 5.0.1 (headless, software EEVEE via Mesa llvmpipe) | **Blender 5.3.0** (GUI, Higgsfield add-on connected) |
| DaVinci Resolve | — | **DaVinci Resolve 21.2.0.6 (free)**, launched by me at 17:03 and running |
| Resolve scripting | — | Module found: `DaVinciResolveScript.py` + `fusionscript.dll`. **`scriptapp("Resolve")` returns None**, so External scripting is disabled in Resolve Preferences (a setting only you can change) |
| Python | 3.13 + 3.11 venv for bpy | **Python 3.12.x** (`py` launcher) |
| FFmpeg / FFprobe | 6.1.1 | Present (WinGet build N-127043) |
| git | present | **present, with GitHub access to this repository (ls-remote OK)** |
| Project folder | `/home/user/OpShot-Studios/THE_GLASS` (git) | `C:\Users\siver\Documents\THE_GLASS` held only 4 files (an earlier SH-031 laptop test) and is not a git checkout |

## What is NOT available
- **Desktop/GUI control (Computer Use / Cowork):** not connected. `list_computer_folders` is empty.
- **Higgsfield host apps:** Blender = connected. After Effects, Premiere Pro, Cinema 4D and 3D Blocking Studio = not connected.
- **Higgsfield credits:** balance **10 credits** on the `ultra` plan. That is not enough for any meaningful video generation, and the spending limit is $0 in any case.
- **Network from the container:** Wikipedia, SNL, Hugging Face and GitHub raw URLs are blocked (fact-checking was done from search summaries).

## File transfer route (cloud → laptop)
The cloud commits to branch `claude/nokas-robbery-script-vwal6c`. The laptop runs `git clone`/`git pull` into
`C:\Users\siver\Documents\THE_GLASS_repo`. Large videos are kept below GitHub's 100 MB per-file limit: the shot clips are 720p at CRF 23, the audio is FLAC, and the 1080p master is rebuilt locally with `09_DELIVERABLES/assemble_from_shots.py`.

## Windows compatibility
- The cloud scripts use `python3`/`bash`. On Windows use `py -3.12 <script>.py`; every builder is plain Python apart from `build_prototype_v001.sh`.
- `09_DELIVERABLES/windows/run_on_laptop.ps1` pulls the repo, rebuilds the 1080p cut and (when scripting is enabled) builds the Resolve timeline.

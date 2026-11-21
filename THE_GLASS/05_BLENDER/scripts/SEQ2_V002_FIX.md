# Fix the frozen end of the 3D 2 "113" v002 reference video

Blender 5.3 renders SH-052 frozen from about frame 110. Blender 5.0.1 renders it correctly.
These steps fetch the official portable Blender 5.0.1 (a zip; your Blender 5.3 is not touched),
check its checksum, and re-render SH-052 frames 106-240 (about 5-10 minutes).

Run in PowerShell:

```powershell
cd $HOME\Documents
Invoke-WebRequest https://download.blender.org/release/Blender5.0/blender-5.0.1-windows-x64.zip -OutFile blender-5.0.1-windows-x64.zip
Invoke-WebRequest https://download.blender.org/release/Blender5.0/blender-5.0.1.sha256 -OutFile blender-5.0.1.sha256
(Get-FileHash blender-5.0.1-windows-x64.zip -Algorithm SHA256).Hash
Select-String blender-5.0.1.sha256 -Pattern "windows-x64.zip"
```
The two long codes must match (upper/lower case does not matter). If they do not, stop and tell Claude.

```powershell
Expand-Archive blender-5.0.1-windows-x64.zip -DestinationPath .
cd $HOME\Documents\THE_GLASS_repo
git pull
& "$HOME\Documents\blender-5.0.1-windows-x64\blender.exe" -b -P THE_GLASS\05_BLENDER\scripts\render_seq2_v002_fix052.py
```
It ends with `WROTE ...SEQ2_113_REFVIDEO_30s_v002.mp4`. Then push it:

```powershell
git add THE_GLASS/06_AI_VIDEO/references/SEQ2_113_REFVIDEO_30s_v002.mp4
git commit -m "3D 2 v002 reference video: SH-052 106-240 re-rendered in Blender 5.0.1"
git push
```

# THE GLASS: laptop launcher (Windows PowerShell)
# 1) clone or update the repo  2) rebuild the 1080p rough cut locally  3) build the Resolve timeline
# Usage (PowerShell):  powershell -ExecutionPolicy Bypass -File run_on_laptop.ps1
$ErrorActionPreference = "Stop"
$Repo   = "$env:USERPROFILE\Documents\THE_GLASS_repo"
$Branch = "claude/nokas-robbery-script-vwal6c"
if (-not (Test-Path "$Repo\.git")) {
    git clone --branch $Branch --single-branch https://github.com/Nebrox-klink/OpShot-Studios.git $Repo
} else {
    git -C $Repo pull --ff-only
}
$Root = "$Repo\THE_GLASS"
py -3.12 "$Root\09_DELIVERABLES\assemble_from_shots.py"
$env:THE_GLASS_ROOT = $Root
$env:RESOLVE_SCRIPT_API = "C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
$env:RESOLVE_SCRIPT_LIB = "C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
$env:PYTHONPATH = "$env:RESOLVE_SCRIPT_API\Modules"
py -3.12 "$Root\08_DAVINCI_RESOLVE\resolve_build_master_timeline_v002.py"
Write-Host "Done. Log: $Root\08_DAVINCI_RESOLVE\resolve_build_v002.log"

# DaVinci Resolve > Workspace > Scripts > Utility > THE_GLASS_build_master_timeline_MENU
# One-click wrapper (works in Resolve free): runs the repo's v002 builder inside Resolve.
import os
ROOT = os.path.join(os.path.expanduser("~"), "Documents", "THE_GLASS_repo", "THE_GLASS")
os.environ["THE_GLASS_ROOT"] = ROOT
src = os.path.join(ROOT, "08_DAVINCI_RESOLVE", "resolve_build_master_timeline_v002.py")
g = dict(globals())
g["__file__"] = src
exec(compile(open(src, encoding="utf-8").read(), src, "exec"), g)

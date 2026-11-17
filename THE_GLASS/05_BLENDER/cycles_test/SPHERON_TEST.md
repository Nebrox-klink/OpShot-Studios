# Cycles test render on Spheron (about 15–20 minutes)

The test renders **5 frames of SH-052** (the glass giving way) at **1920×1080 in Cycles**. The glass is real refractive glass (refraction, crazing, glossy cracks) instead of the flat preview fakes. Every frame is timed, so we learn the real cost before rendering whole scenes.

## 1. Rent the GPU on spheron.network
- Create an account, add credit, and deploy **one RTX 4090** (or similar NVIDIA GPU) running **Ubuntu 22.04 or 24.04**.
- Add your SSH key when Spheron asks. If you have none, run `ssh-keygen` in PowerShell, press Enter at every prompt, and paste the contents of `C:\Users\<you>\.ssh\id_ed25519.pub` into Spheron.
- Note the **IP address** and **username** Spheron shows, often `ubuntu` or `root`.

## 2. Upload the files (PowerShell on your laptop)
```powershell
cd $HOME\Documents\THE_GLASS_repo
git pull
tar -czf glass_test_bundle.tgz THE_GLASS/05_BLENDER/scripts THE_GLASS/05_BLENDER/sequences THE_GLASS/05_BLENDER/cycles_test
scp glass_test_bundle.tgz THE_GLASS/05_BLENDER/cycles_test/spheron_cycles_test.sh USER@IP:~/
```
Replace `USER@IP` with the details from step 1, for example `ubuntu@203.0.113.10`.

## 3. Run the test
```powershell
ssh USER@IP "bash ~/spheron_cycles_test.sh"
```
It shows the GPU, installs Blender, builds the scene and renders the 5 frames. It finishes by printing `timing.json` with the seconds per frame.

## 4. Download the results, then stop the machine
```powershell
scp USER@IP:~/glass_test_results.tgz .
tar -xzf glass_test_results.tgz
```
You now have a `results\` folder with 5 PNG frames, `timing.json` and `gpu.txt`. **Stop or delete the machine in Spheron straight away**, because billing runs until you do.

Push the results so I can look at them and work out the full cost:
```powershell
mkdir THE_GLASS\05_BLENDER\cycles_test\results_spheron -Force
copy results\* THE_GLASS\05_BLENDER\cycles_test\results_spheron\
git add THE_GLASS/05_BLENDER/cycles_test/results_spheron
git commit -m "Spheron Cycles test results"
git push
```

## Options
- More or fewer samples: `ssh USER@IP "SAMPLES=256 bash ~/spheron_cycles_test.sh"` (the default is 128).
- Other frames: `FRAMES=1,120,240`.

## What it costs
On an RTX 4090 at about $0.48/hour, the whole test (setup plus 5 frames) should take 15–20 minutes, so **well under $1**. Spheron may have a minimum top-up.

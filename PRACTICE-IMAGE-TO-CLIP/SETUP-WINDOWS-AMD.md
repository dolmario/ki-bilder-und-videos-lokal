# Windows AMD setup used for the example

Use a new directory for a fresh installation. Our recording reuses the existing working installation; the commands below describe its matching Python/Torch/ComfyUI versions. They are not a claim that the driver and complete environment were freshly installed for this video.

Install 64-bit [Python 3.12](https://www.python.org/downloads/windows/) and [Git](https://git-scm.com/downloads/win). For this ROCm release, follow [AMD's Windows instructions](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/windows/install-pytorch.html), including the matching driver prerequisite. The documented ROCm 7.2.1 driver prerequisite is AMD 26.2.2; that marketing version is not interchangeable with Windows' driver-file number.

Run the commands separately in PowerShell, from a directory you have chosen for this installation:

```powershell
New-Item -ItemType Directory -Path C:\Dolmario-AMD
Set-Location C:\Dolmario-AMD
py -3.12 -m venv venv
.\venv\Scripts\python.exe -m pip install -f https://repo.radeon.com/rocm/windows/rocm-rel-7.2.1/ "torch==2.9.1+rocm7.2.1" "torchvision==0.24.1+rocm7.2.1" "torchaudio==2.9.1+rocm7.2.1"
git clone https://github.com/Comfy-Org/ComfyUI.git
Set-Location ComfyUI
git checkout fa98a189b4271c76f66210e15f81790b555eb610
@('torch==2.9.1+rocm7.2.1','torchvision==0.24.1+rocm7.2.1','torchaudio==2.9.1+rocm7.2.1','rocm==7.2.1') | Set-Content -Encoding ascii torch-pin.txt
..\venv\Scripts\python.exe -m pip install -f https://repo.radeon.com/rocm/windows/rocm-rel-7.2.1/ -c torch-pin.txt -r requirements.txt
..\venv\Scripts\python.exe -m pip check
..\venv\Scripts\python.exe -c "import torch; print(torch.__version__); print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0))"
```

The recorded check prints the AMD Torch build, `True`, and `AMD Radeon(TM) 8060S Graphics`. ROCm uses the `torch.cuda` API too. `True` is a detection check; the supplied image/clip are the separate inference evidence.

Place the eight matching model files as shown in **MODEL-FOLDERS.md**. This example uses standard nodes present in the pinned ComfyUI revision; a GGUF custom node is not part of these graphs.

For the image workflow, start the local UI with:

```powershell
..\venv\Scripts\python.exe main.py --listen 127.0.0.1 --port 8189 --disable-pinned-memory
```

Open `http://127.0.0.1:8189` and import `01-IMAGE.workflow.json` with Ctrl+O. Run the image and keep its PNG for the video input.

On our recorded AMD machine, run the prompt-saving workflow in a separate process using:

```powershell
..\venv\Scripts\python.exe main.py --listen 127.0.0.1 --port 8189 --disable-pinned-memory --gpu-only --disable-dynamic-vram
```

Import `02-PROMPTS.workflow.json`, run it, and move the two `output/conditioning/first-clip-*.safetensors` results to `models/embeddings`, naming them `first-clip-positive.safetensors` and `first-clip-negative.safetensors`. Close that ComfyUI process before returning to the normal start command for the clip.

For the separate clip process on this 64 GB Strix Halo profile, start with:

```powershell
..\venv\Scripts\python.exe main.py --listen 127.0.0.1 --port 8189 --disable-pinned-memory --reserve-vram 16
```

Copy the generated PNG to `input/GENERATED-FIRST-IMAGE.png`, then open `03-CLIP.workflow.json`. Its Load Image and both Load Conditioning names now match those files. The runner in README performs these separate stages automatically into its own new input/output/embeddings directories.

The measured environment is Python 3.12.10, Torch 2.9.1+rocm7.2.1, ComfyUI `fa98a189b4271c76f66210e15f81790b555eb610`, frontend 1.53.10, templates 0.11.74. The same complete setup has not been newly validated on NVIDIA or another AMD GPU.

Primary source for the pinned ComfyUI code: [Comfy-Org/ComfyUI](https://github.com/Comfy-Org/ComfyUI/tree/fa98a189b4271c76f66210e15f81790b555eb610). The commit and Save Conditioning implementation were checked against the public GitHub API/raw file on 11 October 2026.

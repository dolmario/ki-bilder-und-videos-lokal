# Your first LTX-2.5 clip on Strix Halo

Turn the supplied portrait PNG into a five-second silent clip. The portrait was generated in our separate FLUX.2 tutorial. This kit computes its own new positive and negative motion conditioning with Gemma, releases that process, then runs both LTX video passes. It uses only standard nodes in the pinned ComfyUI source.

## Install a separate source folder

Use the Python from your existing working AMD environment. The installer downloads the official pinned ComfyUI source archive into a new folder and verifies its checksum and every installed file. It reuses your driver and PyTorch installation. Python, FFmpeg, psutil and Pillow must already be available; the recorded versions are in ENVIRONMENT.json.

```powershell
py -3.12 install_sources.py --python C:\AI\venv\Scripts\python.exe --output my-ltx-sources
```

Place the five files from MODELS.json into your model directory: diffusion_models, text_encoders, vae and latent_upscale_models. Existing files are checked in full by the runner. The model weights are separate downloads; download_models.py can fetch them with checksum verification.

```powershell
py -3.12 download_models.py --output C:\Models
```

## Run the portrait example

```powershell
C:\AI\venv\Scripts\python.exe run_clip.py --comfyui .\my-ltx-sources\ComfyUI --python C:\AI\venv\Scripts\python.exe --models C:\Models --output my-first-ltx-clip
```

The runner verifies the five model files, creates a new output directory, computes text in a separate GPU-only process, stops it, then runs the video graph with the recorded 16 GiB reserve. The graph starts at 512×512, 121 frames and 24 fps, then enlarges the latent 2× and refines it. The saved H.264 clip is 1024×1024, 121 frames, about 5.04s and silent. The audio latent branch is part of the LTX graph; this export uses only the video frames.

Choose a new output directory for each run. Existing files are preserved. The runner stops only its own child processes; close your own other model work before starting. This is the profile measured on our 64 GB Strix Halo Windows machine. It has not been validated on NVIDIA or a smaller GPU.

## Work directly in ComfyUI

Copy model-paths.example.yaml to model-paths.yaml, set your model directory and an absolute new manual-run directory. Make input, output, user and embeddings subfolders. Copy example/PORTRAIT.png into input. Keep your kit and model folders separate.

```powershell
$ltxPython = 'C:\AI\venv\Scripts\python.exe'
& $ltxPython .\my-ltx-sources\ComfyUI\main.py --listen 127.0.0.1 --port 8188 --disable-pinned-memory --gpu-only --disable-dynamic-vram --input-directory C:\AI\LTX\manual-run\input --output-directory C:\AI\LTX\manual-run\output --user-directory C:\AI\LTX\manual-run\user --extra-model-paths-config C:\AI\LTX\model-paths.yaml
```

Open http://127.0.0.1:8188 and import 00-TEXT.json with Ctrl+O. Edit the motion text and press Run. After both Save Conditioning nodes finish, stop that console with Ctrl+C. Copy output/conditioning/first-clip-positive_00001_.safetensors and first-clip-negative_00001_.safetensors into embeddings, naming them first-clip-positive.safetensors and first-clip-negative.safetensors.

Start the same command again, replacing --gpu-only --disable-dynamic-vram with --reserve-vram 16. Refresh the browser, import 01-CLIP.json and select both conditioning files. If the frontend still reports a missing conditioning file, open its issue details and click Refresh. Choose PORTRAIT.png at Load Image and press Run. Right-click the completed Save Video preview to download the clip. The input picture, motion text, size and seed remain with the output history.

For a different picture, change the Load Image input and describe its movement in the text graph. Compute fresh conditioning before selecting it in the video graph. Keep width and height aligned with your picture and start with the recorded settings before changing one control at a time.

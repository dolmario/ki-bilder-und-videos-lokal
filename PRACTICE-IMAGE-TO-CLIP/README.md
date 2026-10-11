# Make an image, then turn it into a clip

Create the copper-roofed town with FLUX.2 Klein, then animate that actual PNG with LTX. The folder contains three connected workflows, a runner for separate model stages, and the complete example image and five-second MP4.

Open **SETUP-WINDOWS-AMD.md** for the installation commands and **MODEL-FOLDERS.md** for the exact eight model files. Open the `.workflow.json` files with **Ctrl+O** in ComfyUI. The `.api.json` files are the runner's inputs.

## Run the complete example

Use the Python from your existing ComfyUI environment. The example below uses an installation at `C:\Dolmario-AMD`:

```powershell
C:\Dolmario-AMD\venv\Scripts\python.exe .\run_example.py --comfyui C:\Dolmario-AMD\ComfyUI --output .\my-image-and-clip
```

The runner verifies all eight model files, then starts a separate local ComfyUI process for each stage:

1. `01-IMAGE`: generate `results/IMAGE.png` and copy it to the video input.
2. `02-PROMPTS`: encode the positive and negative motion texts once, save the conditioning, and close that process. On our AMD machine this stage uses `--gpu-only --disable-dynamic-vram`.
3. `03-CLIP`: load the saved conditioning and starting image, run both video passes, and save `results/CLIP.mp4`. This 64 GB Strix Halo profile keeps 16 GiB out of the video model budget with `--reserve-vram 16`; `--clip-reserve-vram` changes that runner value. It is not a preset validated on smaller dedicated GPUs.

Choose a new output folder for another run. The runner preserves existing folders. Its default port is `18189`; `--port` selects another free port. It stops only the processes it starts. Finish other GPU jobs before running the example. It does not stop a Wiki, router, or another ComfyUI instance for you.

For a file check without model inference:

```powershell
C:\Dolmario-AMD\venv\Scripts\python.exe .\run_example.py --comfyui C:\Dolmario-AMD\ComfyUI --check
```

## Follow the workflows in the UI

`01-IMAGE.workflow.json` shows the model, text encoder and VAE on the left. The prompt enters the guider; the sampler output enters VAE Decode and Save Image. The example uses four steps, guidance `1`, seed `11`, and `1536 × 864` pixels.

`02-PROMPTS.workflow.json` connects each motion text to Save Conditioning. Move those saved files into your `models/embeddings` folder before opening the third workflow. The runner instead registers an embeddings folder inside its own new output directory.

`03-CLIP.workflow.json` loads the PNG and both conditioning files. It starts at `640 × 352`, `121` frames and `24 fps`, then doubles the latent resolution before three refinement steps. Export is a **silent H.264 MP4, 1280 × 704, 5.04 seconds**. The video/audio latent branch and both VAEs are part of the LTX graph; this example saves video frames without a soundtrack.

To make a different scene, edit the image prompt in `workflows/01-IMAGE.api.json` and the motion texts in `workflows/02-PROMPTS.api.json`, then run into another new folder. In the UI, edit the corresponding prompt boxes and generate fresh conditioning whenever the motion text changes.

## Example and measured environment

`example/IMAGE.png` is the input of `example/CLIP.mp4`. `example/RUN.json` records the executed graphs, hashes and measured stage times. The recorded machine is a 64 GB Strix Halo PC under Windows, with 32 GB reserved for the iGPU. Its Windows and device-memory figures refer to physically shared memory.

The supplied example was produced with the installed, recorded environment. A completely new AMD driver/Python installation was not performed for this recording. Public runner validation and any additional runs are listed in `VALIDATION.json`; that record distinguishes graph execution from a fresh installation.

The package contains our prompts, workflows and generated example, **no model weights**. Models retain their source terms; the download table links the model repositories. This example does not establish a universal RAM requirement or performance claim for other GPUs.

## Deutsch

Erzeuge zuerst die Stadt mit FLUX.2 Klein und animiere anschließend genau diese PNG mit LTX. Die drei Workflows liegen unter `workflows`; mit **Strg+O** lassen sie sich in ComfyUI öffnen. `MODEL-FOLDERS.md` nennt die acht tatsächlich verwendeten Dateien samt Ordnern und SHA256. `SETUP-WINDOWS-AMD.md` enthält die passenden Einrichtungsbefehle.

Der Runner verwendet nacheinander einen Prozess für das Bild, einen für die gespeicherten Prompts und einen für den Clip. Er erzeugt einen neuen Ausgabeordner und beendet ausschließlich seine eigenen Prozesse. Ergebnis: `results/IMAGE.png` plus ein stummer Clip mit 121 Frames bei 24 fps. Das vollständige Beispiel liegt unter `example`.

Beim Ändern des Bewegungstextes muss die Conditioning neu erzeugt werden. Große Modellgewichte gehören nicht zum ZIP; die verlinkten Quellen und deren Bedingungen gelten weiterhin.

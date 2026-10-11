# LTX-2.5: five seconds or ten?

Use the same starting PNG, fixed seed, motion conditioning, size and two-pass graph; change only the frame count. The five-second clip comes from our earlier executed portrait tutorial. The ten-second example is a separate newly sampled run. It is not an extension made by looping or slowing the first clip.

## Set up and run

The source installer downloads the pinned official ComfyUI archive into a new folder. Use your existing working AMD Python environment; driver and PyTorch are reused. Put the four models from MODELS.json into diffusion_models, vae and latent_upscale_models. The saved positive/negative conditioning is supplied, so this comparison does not load Gemma again.

```powershell
py -3.12 install_sources.py --python C:\AI\venv\Scripts\python.exe --output my-length-sources
C:\AI\venv\Scripts\python.exe run_clip.py --comfyui .\my-length-sources\ComfyUI --python C:\AI\venv\Scripts\python.exe --models C:\Models --output my-ten-second-clip
```

The default uses 241 frames at 24 fps, about 10.04 seconds. The graph starts at 512×512 and refines to 1024×1024. The MP4 is silent. `--frames 121` selects the five-second frame count in a new output folder (write the flag and value separated: --frames 121). The earlier five-second execution and the new ten-second execution have separate histories and timings; they are individual runs on our 64 GB Strix Halo Windows setup, not universal performance figures.

## Follow the graph in ComfyUI

Copy the supplied PNG to input and both example/conditioning files into your registered embeddings directory. Start the native video process with `--disable-pinned-memory --reserve-vram 16`, using the model path configuration from the first-clip guide. Import `01-CLIP.json`. At Empty LTX Video set `length` to 241; at Empty Latent Audio set `frames_number` to 241. Keep both frame rate fields at 24, size 512×512 and seed 11/fixed in both noise nodes. Press Run and keep the resulting MP4 beside its history.

The unchanged motion text is recorded in the baseline tutorial; new words require new text encoding before using the video graph. The runner intentionally reuses the supplied conditioning to keep this length comparison consistent.

The memory guard independently records physical availability and available commit. It stops its own process after five seconds below 4 MiB physical, or below 256 MiB physical together with less than 2 GiB available commit. No Windows/pagefile setting is changed. Close your own other model work first; this runner never stops someone else's process.

For new words, use the separate text step in the [first LTX portrait guide](https://github.com/dolmario/ki-bilder-und-videos-lokal/tree/praxis-comfy-bild-video-20261010/PRACTICE-FIRST-LTX-CLIP). This kit deliberately keeps that already executed motion text unchanged.

The recorded ten-second refinement took substantially longer per step than the five-second reference. The runner allows 60 minutes for the video job; this is a timeout, not a promised runtime. Keep each measured run beside its history.

The `views` folder contains the same connected graph with different saved canvas focus positions. Import a view for enlarged input, size, conditioning, sampling or model fields; these change the view, not the graph settings.

## Recorded native video runs

The earlier 121-frame video ran in 593.609s (about 9m54s); the new 241-frame video ran in 2120.295s (about 35m20s). These are video-only measurements from our individual recorded runs. The new longer run reuses the earlier saved text conditioning and does not perform another text encoding. Both use the same recorded spatial profile and 16 GiB reserve.

# Model files and folders

These are the eight exact files used for this example. Sizes refer to disk files, not GPU-memory requirements. Together they occupy 52.16 GB (48.58 GiB) before the Python environment.

Place each file under `ComfyUI/models/` in the folder shown. The LTX repository requires its own access/terms acceptance; sign in on the official model page before downloading its files. Weights are not included in this kit.

| Folder and filename | GB on disk | Exact tested download |
|---|---:|---|
| `diffusion_models/flux-2-klein-4b-fp8.safetensors` | 4.07 | [download](https://huggingface.co/black-forest-labs/FLUX.2-klein-4b-fp8/resolve/5b4408e59397a4a37ccb46afe426d8ed86379441/flux-2-klein-4b-fp8.safetensors) |
| `text_encoders/qwen_3_4b.safetensors` | 8.04 | [download](https://huggingface.co/Comfy-Org/vae-text-encorder-for-flux-klein-4b/resolve/5f526678002e43af5551dadb73ce2e8c91b43afe/split_files/text_encoders/qwen_3_4b.safetensors) |
| `vae/flux2-vae.safetensors` | 0.34 | [download](https://huggingface.co/Comfy-Org/flux2-dev/resolve/ed33133cd56476eac818c0943b6f9419b3e4a3a1/split_files/vae/flux2-vae.safetensors) |
| `diffusion_models/ltx-2.5-22b-distilled-transformer-comfy-int8-convrot.safetensors` | 21.50 | [download](https://huggingface.co/Lightricks/LTX-2.5/resolve/2356ce76915d6c48d313d7e8b25900e1dd3abaa8/diffusion_models/ltx-2.5-22b-distilled-transformer-comfy-int8-convrot.safetensors) |
| `text_encoders/gemma4-12b-with-proj-ltx-2.5-comfy-int8-convrot.safetensors` | 15.37 | [download](https://huggingface.co/Lightricks/LTX-2.5/resolve/2356ce76915d6c48d313d7e8b25900e1dd3abaa8/text_encoders/gemma4-12b-with-proj-ltx-2.5-comfy-int8-convrot.safetensors) |
| `vae/ltx-2.5-video-vae-bf16.safetensors` | 1.47 | [download](https://huggingface.co/Lightricks/LTX-2.5/resolve/2356ce76915d6c48d313d7e8b25900e1dd3abaa8/vae/ltx-2.5-video-vae-bf16.safetensors) |
| `vae/ltx-2.5-audio-vae-bf16.safetensors` | 0.36 | [download](https://huggingface.co/Lightricks/LTX-2.5/resolve/2356ce76915d6c48d313d7e8b25900e1dd3abaa8/vae/ltx-2.5-audio-vae-bf16.safetensors) |
| `latent_upscale_models/ltx-2.5-latent-spatial-upscaler-x2-bf16-1.0.safetensors` | 1.00 | [download](https://huggingface.co/Lightricks/LTX-2.5/resolve/2356ce76915d6c48d313d7e8b25900e1dd3abaa8/latent_upscale_models/ltx-2.5-latent-spatial-upscaler-x2-bf16-1.0.safetensors) |

`MODELS.json` contains the full SHA256, size and pinned repository revision for every file. The runner checks them before inference.

The VAE here is the exact tested file from `Comfy-Org/flux2-dev`; the video encoder is the linked official LTX conversion.

Model terms: [Klein model card](https://huggingface.co/black-forest-labs/FLUX.2-klein-4b-fp8), [Qwen encoder conversion](https://huggingface.co/Comfy-Org/vae-text-encorder-for-flux-klein-4b), [tested VAE source](https://huggingface.co/Comfy-Org/flux2-dev), [LTX model card and license](https://huggingface.co/Lightricks/LTX-2.5). Model weights retain the terms of their sources.

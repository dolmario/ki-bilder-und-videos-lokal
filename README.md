# ComfyUI: create an image and turn it into a clip

Make a copper-roofed town with FLUX.2 Klein, then animate that exact PNG with LTX. The practical example has three ready-to-open workflows, a runner for the separate model stages, and the complete image/clip pair.

![Our actual generated starting image](PRACTICE-IMAGE-TO-CLIP/example/IMAGE.png)

**[Download the complete practice kit](downloads/IMAGE-TO-CLIP-KIT.zip)** · [Walkthrough](PRACTICE-IMAGE-TO-CLIP/README.md) · [Windows AMD setup](PRACTICE-IMAGE-TO-CLIP/SETUP-WINDOWS-AMD.md) · [Exact models and folders](PRACTICE-IMAGE-TO-CLIP/MODEL-FOLDERS.md)

| Stage | Open in ComfyUI | Runner input |
|---|---|---|
| Generate the image | [Image workflow](PRACTICE-IMAGE-TO-CLIP/workflows/01-IMAGE.workflow.json) | [API graph](PRACTICE-IMAGE-TO-CLIP/workflows/01-IMAGE.api.json) |
| Save the motion prompts | [Prompt workflow](PRACTICE-IMAGE-TO-CLIP/workflows/02-PROMPTS.workflow.json) | [API graph](PRACTICE-IMAGE-TO-CLIP/workflows/02-PROMPTS.api.json) |
| Produce the clip | [Clip workflow](PRACTICE-IMAGE-TO-CLIP/workflows/03-CLIP.workflow.json) | [API graph](PRACTICE-IMAGE-TO-CLIP/workflows/03-CLIP.api.json) |

Open the UI files with **Ctrl+O**. For the full run, follow the command in the walkthrough. The runner creates a new output folder, verifies the eight exact model files and uses a separate owned ComfyUI process for each stage. The measured example exports a silent 121-frame H.264 MP4 at 24 fps, 1280 × 704 pixels.

[Example execution record](PRACTICE-IMAGE-TO-CLIP/example/RUN.json) · [Validation](PRACTICE-IMAGE-TO-CLIP/VALIDATION.json) · [File manifest](PRACTICE-IMAGE-TO-CLIP/MANIFEST.json)

## Existing hardware packages

The earlier packages and their archive remain available:

| Machine | Deutsch | English |
|---|---|---|
| Strix Halo | [HALO-DE.zip](HALO-DE.zip) | [HALO-EN.zip](HALO-EN.zip) |
| RTX 3080 Ti | [3080TI-DE.zip](3080TI-DE.zip) | [3080TI-EN.zip](3080TI-EN.zip) |
| RTX 3090 Ti | [3090TI-DE.zip](3090TI-DE.zip) | [3090TI-EN.zip](3090TI-EN.zip) |

[Earlier English guide](START-EN.md) · [Frühere deutsche Anleitung](START-DE.md) · [Archive](ARCHIV)

## Deutsch

Das neue Praxisbeispiel erzeugt zunächst die Stadt mit FLUX.2 Klein und macht anschließend aus genau diesem Startbild einen LTX-Clip. Im ZIP liegen die drei Workflows, die passenden Befehle und das vollständige Bild-Clip-Paar. Die Modellgewichte werden separat aus den verlinkten Quellen geladen. Einrichtungsstand und tatsächlich geprüfte Ausführungen stehen im Validierungsnachweis.

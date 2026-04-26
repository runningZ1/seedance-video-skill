# Seedance 2.0 Video Generation Skill

> 中文文档: [README.md](README.md)

CLI toolkit for Seedance 2.0 video generation workflows on [Volcengine Ark](https://www.volcengine.com/product/ark) Video Generation API.

## What It Does

1. Text-to-video generation
2. Image-to-video generation
3. Multimodal reference generation (text + image + video + audio)
4. Video editing and extension
5. Draft-to-final workflow
6. Web search for text-only tasks
7. Automatic async task polling

## Entry Command

```bash
python scripts/seedance_cli.py --help
```

Main commands:

- `video`: full-featured video workflow
- `image-to-video`: quick image-to-video workflow

## Quick Start

### Text-to-video

```bash
python scripts/seedance_cli.py video \
  --model doubao-seedance-2-0-260128 \
  --prompt "A glass frog on tropical leaves after rain, macro lens, morning light" \
  --ratio 16:9 \
  --duration 5 \
  --generate-audio
```

### Image-to-video

```bash
python scripts/seedance_cli.py image-to-video \
  --prompt "Generate a product ad shot based on the input images" \
  --image-url "https://example.com/product_front.png" \
  --image-file "D:/materials/product_back.png" \
  --ratio 1:1 \
  --duration 6
```

## Setup

### Windows

```powershell
cd scripts/init_dev_env
.\setup_windows.ps1
# or
python ..\init_environment.py --quiet
```

### macOS / Linux

```bash
cd scripts/init_dev_env
./setup_mac.sh
# or
python ../init_environment.py --quiet
```

## Environment

- `ARK_API_KEY` in `.env` or system env
- Python 3.10+
- Public URLs are recommended for media input

## Boolean Flags

Switch behavior is simple:

- include the flag => enabled
- omit the flag => disabled

Examples: `--web-search`, `--camera-fixed`, `--watermark`, `--no-poll`

For audio:

- `--generate-audio` to enable
- `--no-generate-audio` to disable explicitly

## Notes

- Task metadata and output URLs usually expire in ~24 hours.
- Large assets should use public URLs to avoid oversized requests.
- For deeper API details and prompt templates, see:
  - `references/api-workflow.md`
  - `references/prompt-playbook.md`

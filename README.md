# Seedance 2.0 Video Generation Skill

A Claude Code skill for generating, editing, and extending videos with [Volcengine Ark](https://www.volcengine.com/product/ark) Seedance 2.0 via the Video Generation API.

## Overview

This skill enables Claude Code agents to orchestrate complete Seedance 2.0 video workflows: prompt design, multimodal content assembly (text / image / video / audio), async task management with polling, and production-ready output handling.

Supported task types:

| Type | Description |
|---|---|
| **Text-to-video (T2V)** | Generate video from a text prompt only |
| **Image/multimodal reference (R2V)** | Reference 0–9 images, 0–3 videos, 0–3 audios to guide generation |
| **Video editing (V2V)** | Add, remove, or replace elements in an existing video |
| **Video extension** | Extend a clip forward or backward, or connect 2–3 clips with generated transitions |
| **Web search** | Live web search for time-sensitive text-only prompts |
| **Draft-to-final** | Two-step flow: create draft first, then finalize from draft task ID |

## Models

| Model ID | Quality | Max Resolution | Use when |
|---|---|---|---|
| `doubao-seedance-2-0-260128` | Highest | 1080p | Default — quality-critical tasks |
| `doubao-seedance-2-0-fast-260128` | Fast | 720p | Speed or cost-sensitive tasks |

Both models support: T2V, I2V, multimodal reference, video edit/extend, web search, audio generation, and last-frame return.

## Repository Structure

```
seedance-video-skill/
├── SKILL.md                           # Claude Code skill definition (entry point)
├── .env                               # API keys and model constants
├── agents/
│   └── openai.yaml                    # Agent interface metadata
├── scripts/
│   ├── seedance_cli.py               # Unified CLI entrypoint (recommended)
│   ├── run_seedance_task.py           # Main CLI — create & poll any Seedance task
│   ├── run_seedance_image_to_video.py # Dedicated image-to-video wrapper
│   ├── run_duomi_nano_banana_text2img.py # Text-to-image via Duomi API (fallback)
│   ├── init_environment.py            # One-time Python environment setup
│   ├── preview.html                   # Demo preview
│   └── init_dev_env/
│       ├── setup_windows.ps1          # Windows PowerShell setup
│       ├── setup_windows.bat          # Windows CMD setup
│       └── setup_mac.sh               # macOS/Linux setup
├── references/
│   ├── api-workflow.md                # API payload, polling, parameters, limits
│   ├── prompt-playbook.md             # Prompt templates and multimodal reference guide
└── outputs/                           # Generated task results (JSON, MP4, PNG)
```

## Prerequisites

- **ARK_API_KEY** — Volcengine Ark API key (set in `.env` or environment)
- Account balance ≥ 200 CNY, or a resource pack purchased on Ark console
- Python 3.10+
- Public URLs for input media (image / video / audio), or local files (auto-converted to base64, max 30 MB)

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

Setup creates a `.venv` virtual environment, installs `volcengine-python-sdk[ark]`, and generates convenience run scripts (`seedance.bat` / `seedance.sh`).

### Recommended unified CLI

```bash
python scripts/seedance_cli.py --help
```

You can still call old scripts directly, but `seedance_cli.py` is the single entrypoint for faster command discovery.

## Usage

### Text-to-video

```bash
python scripts/seedance_cli.py video run \
  --model doubao-seedance-2-0-260128 \
  --prompt "一只玻璃蛙栖息在雨后的热带叶片上，微距镜头，晨光折射" \
  --ratio 16:9 \
  --duration 5 \
  --generate-audio true
```

### Image-to-video (R2V)

```bash
python scripts/seedance_cli.py video run \
  --prompt "参考 图片1 和 图片2 中的产品，白色背景，以产品为主体缓慢旋转展示正面侧面背面" \
  --image-url "https://example.com/product_front.png" \
  --image-file "D:/materials/product_back.png" \
  --ratio 1:1 \
  --duration 6
```

### Video editing (V2V)

```bash
python scripts/seedance_cli.py video run \
  --prompt "将 视频1 中的香水替换成 图片1 中的面霜，动作和运镜不变" \
  --video-url "https://example.com/original.mp4" \
  --image-file "D:/materials/cream.png" \
  --ratio 16:9 \
  --duration 5
```

### Video extension (track-fill, 3 clips)

```bash
python scripts/seedance_cli.py video run \
  --prompt "视频1中的拱形窗户打开，进入美术馆室内，接视频2，之后镜头进入画内，接视频3" \
  --video-url "https://example.com/clip1.mp4" \
  --video-url "https://example.com/clip2.mp4" \
  --video-url "https://example.com/clip3.mp4" \
  --ratio 16:9 \
  --duration 10
```

> Note: Max 3 clips for track-fill. Total output ≤ 15 seconds. The model auto-clips join segments; original input content is preserved (not regenerated).

### Web search (text-only)

```bash
python scripts/seedance_cli.py video run \
  --prompt "微距镜头对准叶片上翠绿的玻璃蛙，联网搜索玻璃蛙的容貌特征。" \
  --web-search \
  --ratio 16:9 \
  --duration 11
```

### Draft-to-final

```bash
# Step 1: create draft
python scripts/seedance_cli.py video run \
  --model doubao-seedance-2-0-260128 \
  --prompt "..." \
  --draft

# Step 2: finalize from draft task ID
python scripts/seedance_cli.py video run \
  --model doubao-seedance-2-0-260128 \
  --draft-task-id cgt-xxxx
```

## Prompt Design

Prompts follow this structure (required → optional):

```
[主体 + 动作] → [场景 + 风格] → [运镜] → [音频] → [输出约束]
```

### Key rules

- **Multimodal references** use ordinal tokens by upload order within each modality: `图片1`, `图片2`, `视频1`, `音频1`. Never reference by asset ID.
- **Common characters only** for on-screen text — avoid rare symbols for best rendering.
- **Logo/brand text fidelity**: supply the logo as an image asset and reference it with `画面逐渐模糊，后出现图片1的Logo。` rather than describing text in the prompt.

### Common prompt templates

**Slogan / advertising text:**
```
「文字内容」+「出现时机」+「出现位置」+「出现方式」，「文字特征（颜色、风格）」
```

**Subtitle sync:**
```
画面底部出现字幕，字幕内容为"……"，字幕需与音频节奏完全同步。
```

**Speech bubble:**
```
「角色」说："……"，角色说话时周围出现气泡，气泡里写着台词。
```

**Multi-angle product showcase:**
```
提取 图片1、图片2、图片3 的[产品]，背景换成[背景]，以[产品]为主体缓慢旋转，清晰展示正面侧面背面。
```

**Multi-element assembly:**
```
图片1中的[角色]身着图片2中的[服装]，在图片4中的[场景]内，[动作]。图片5中的[标识]始终显示在画面[位置]。
```

See [references/prompt-playbook.md](references/prompt-playbook.md) for the full template library.

## Key Parameters

| Parameter | CLI flag | Notes |
|---|---|---|
| Model | `--model` | See models table above |
| Prompt | `--prompt` | Text instruction |
| Image (URL) | `--image-url` | Can repeat; up to 9 total |
| Image (local) | `--image-file` | Auto base64, max 30 MB |
| Video (URL) | `--video-url` | Can repeat; up to 3 total |
| Audio (URL) | `--audio-url` | Can repeat; up to 3 total |
| Resolution | `--resolution` | `480p`, `720p`, `1080p` (quality model only) |
| Aspect ratio | `--ratio` | `adaptive`, `16:9`, `9:16`, `1:1`, `4:3`, `21:9` |
| Duration | `--duration` | 4–15 seconds |
| Seed | `--seed` | Reproducibility |
| Generate audio | `--generate-audio` | Bool |
| Return last frame | `--return-last-frame` | For chaining tasks |
| Web search | `--web-search` | Text-only tasks |
| Batch mode | `--service-tier flex` | Lower cost, not real-time |
| Output JSON | `--output-json` | Persist result to file |

## Production Guardrails

- **24-hour retention**: Task metadata and generated video URLs expire after ~24 hours. Move outputs to persistent storage (e.g. TOS) promptly.
- **Face policy**: Direct upload of real human face images/videos is blocked. Use (a) platform virtual avatar assets (`asset://<asset-id>`), (b) same-account Seedance/Seedream outputs within 30 days (trusted outputs bypass face check), or (c) authorized real-person assets registered via Ark console.
- **Aspect ratio mismatch**: Image-to-video triggers center-crop when input ratio differs from target ratio.
- **Request size**: Single image ≤ 30 MB; total request body ≤ 64 MB. Prefer URL input over base64 for large assets.
- **Rate limits**: Enterprise — 600 RPM, 10 concurrent tasks; Personal — 180 RPM, 3 concurrent tasks.

## References

- [API Workflow & Parameters](references/api-workflow.md)
- [Prompt Playbook & Templates](references/prompt-playbook.md)
- [Volcengine Ark Video Generation Docs](https://www.volcengine.com/docs/82379/2291680?lang=zh)
- [Seedance 2.0 Prompt Guide](https://www.volcengine.com/docs/82379/2222480?lang=zh)

## Changelog

### 2026-04-26
- Updated `references/prompt-playbook.md` based on official Doubao Seedance 2.0 Prompt Guide:
  - Restructured to match official guide sections (文字生成, 图片参考, 视频参考, 视频编辑)
  - Added dedicated on-screen text section: slogan, subtitle sync, multi-person dialogue, speech bubble
  - Expanded image reference section: multi-angle product reference, logo pattern, multi-subject, multi-element assembly, storyboard/grid reference
  - Split video reference into action / camera / effects subsections with individual templates
  - Added video extension note: model auto-clips join segments, original input preserved
  - Added logo/brand text fidelity guidance: use logo-as-image-asset pattern
- Updated `SKILL.md` step 3 with concrete prompt templates for slogan, subtitle, logo, product, and multi-element assembly use cases
- Added video extension auto-clip behavior note to task type decision step

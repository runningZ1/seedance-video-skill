---
name: seedance-video-generation
description: Use this skill when Codex needs to create, edit, or extend videos with Volcengine Ark Seedance 2.0 / 2.0 fast via Video Generation API, including prompt design, multimodal content assembly (text/image/video/audio), task polling, output spec control (resolution/ratio/duration/seed/camera_fixed/watermark), and production guardrails such as 24-hour URL retention and asset persistence.
---

# Seedance 2.0 Video Generation

Implement Seedance video workflows with a deterministic API-first process: build content payload, create async task, poll status, and return downloadable result URLs.

Use `scripts/run_seedance_task.py` for execution and read targeted references only when needed.

## Workflow

1. Confirm prerequisites.
- Require `ARK_API_KEY` in environment.
- `scripts/run_seedance_task.py` auto-loads `seedance-video-generation/.env` before reading env vars.
- Choose `model` (`doubao-seedance-2-0-260128` for quality, `doubao-seedance-2-0-fast-260128` for speed/cost).
- For images, use URL or local file (`--image-file`, auto-base64). For videos, keep URL input.
- Ensure media URLs are publicly accessible.

2. Decide task type from user request.
- Text to video: prompt only.
- Image/video/audio referenced generation (multimodal R2V): add any combo of `reference_image` (0–9), `reference_video` (0–3), `reference_audio` (0–3). Not supported: text+audio only, audio-only.
- Video edit: prompt + `reference_video` as the source, optionally add `reference_image` / `reference_audio` for replacement elements.
- Video extend (forward/backward/track-fill): prompt + 1–3 `reference_video` items. Total output ≤ 15 s. Model auto-clips join segments; original input content is preserved (not regenerated).
- Strict first/last frame lock: use roles `first_frame` / `last_frame` on image items.
- Virtual avatar or authorized real-person asset: use `asset://<asset-id>` as the URL; refer in prompt by ordinal (e.g., `图片1`).
- Web search (text-only): add `tools=[{"type": "web_search"}]`; model decides whether to search.

3. Draft high-quality prompt.
- Keep clear subject-action-scene-camera-audio logic.
- Use precise reference mentions: `图片1/图片2` and `视频1/视频2` based on upload order within each modality.
- Prefer common characters for on-screen text; avoid rare symbols and special characters.
- For slogan/advertising text: `「文字内容」+「出现时机」+「出现位置」+「出现方式」，「文字特征」`
- For subtitle sync: `画面底部出现字幕，字幕内容为"……"，字幕需与音频节奏完全同步。`
- For bubble text: `「角色」说："…"，角色说话时周围出现气泡，气泡里写着台词。`
- For strict logo/brand text fidelity: supply logo as an image asset and use `画面逐渐模糊，后出现图片1的Logo。`
- For multi-angle product reference: upload 2–3 angle images and `提取 图片1、图片2、图片3 的[产品]，以[产品]为主体缓慢旋转，清晰展示正面侧面背面。`
- For multi-element assembly: `图片1中的[角色]身着图片2中的[服装]，在图片4中的[场景]内，图片5中的[标识]始终显示在画面[位置]。`
- For track-fill: `视频1，[过渡描述]，接视频2，[过渡描述]，接视频3。` (max 3 clips, total ≤ 15s; model auto-clips join segments, input not re-generated)
- For all templates and examples, read `references/prompt-playbook.md`.

4. Build request and submit task.
- Prefer explicit request fields over appending `--params` in prompt text.
- Start with `ratio="adaptive"` unless composition requires fixed ratio.
- Set `resolution`, `ratio`, `duration` (4–15 s), `seed`, `camera_fixed`, `watermark` explicitly when requested.
- Add `return_last_frame="true"` when the output frame is needed for chaining tasks.
- Add `service_tier="flex"` for offline/batch workloads to reduce cost.
- Add `tools=[{"type": "web_search"}]` for time-sensitive text-only prompts (e.g., current events).

5. Poll until terminal status.
- Poll `content_generation.tasks.get(task_id=...)` every 10-30 seconds.
- Handle terminal states `succeeded`, `failed`, `expired`.
- On success, return `content.video_url` and include `content.last_frame_url` when present.

6. Apply production guardrails.
- Warn that task data and generated URLs are retained for only 24 hours.
- Recommend moving outputs to persistent storage (for example TOS) before expiry.
- If image ratio and target ratio differ, note center-crop behavior.
- Real human face inputs are blocked. Options: (a) use platform virtual avatar assets (`asset://`), (b) reuse same-account Seedance/Seedream model outputs within 30 days (trusted outputs bypass face check), (c) register authorized real-person assets via Ark console.

## Environment Setup

The skill is fully self-contained. Initialize the environment once:

### Windows (PowerShell)

```powershell
# Navigate to scripts/init_dev_env folder
cd scripts/init_dev_env

# Run PowerShell setup
.\setup_windows.ps1

# Or use Python (cross-platform)
python ../init_environment.py
```

After setup, run:
- `.\seedance.ps1` (PowerShell) - Quick start with examples
- `seedance.bat` (CMD) - Alternative quick start

### macOS / Linux

```bash
# Navigate to scripts/init_dev_env folder
cd scripts/init_dev_env

# Run shell setup
./setup_mac.sh

# Or use Python (cross-platform)
python ../init_environment.py
```

After setup, run:
- `./seedance.sh` - Quick start with examples

### All Platforms (Python, cross-platform)

```bash
# Python 3.10+ required
python scripts/init_environment.py

# Or non-interactive mode (faster, uses uv if available)
python scripts/init_environment.py --quiet
```

This will:
1. Create a virtual environment (`.venv`)
2. Install `volcengine-python-sdk[ark]`
3. Generate convenient run scripts

## Quick Commands

Python helper (recommended):

```bash
python scripts/run_seedance_task.py \
  --model doubao-seedance-2-0-260128 \
  --prompt "将视频1礼盒中的香水替换成图片1中的面霜，运镜不变" \
  --video-url "https://.../input.mp4" \
  --image-file "D:/materials/cream.png" \
  --ratio 16:9 \
  --duration 5 \
  --watermark true \
  --generate-audio true
```

Local image + URL image mixed input (order: URL first, then local file):

```bash
python scripts/run_seedance_task.py \
  --prompt "参考图片1和图片2，生成产品广告镜头" \
  --image-url "https://.../ref1.png" \
  --image-file "D:/materials/ref2.png"
```

Video extension (connect 3 clips with transitions):

```bash
python scripts/run_seedance_task.py \
  --prompt "视频1中的拱形窗户打开，进入美术馆室内，接视频2，之后镜头进入画内，接视频3" \
  --video-url "https://.../clip1.mp4" \
  --video-url "https://.../clip2.mp4" \
  --video-url "https://.../clip3.mp4" \
  --ratio 16:9 \
  --duration 8
```

Web search enabled (text-only):

```bash
python scripts/run_seedance_task.py \
  --prompt "微距镜头对准叶片上翠绿的玻璃蛙，联网搜索玻璃蛙的容貌特征。" \
  --ratio 16:9 \
  --duration 11
```

Draft to final flow (if user requests sample mode):

```bash
# Step 1: create draft
python scripts/run_seedance_task.py --prompt "..." --model doubao-seedance-2-0-260128 --draft
# Step 2: create final by draft task id
python scripts/run_seedance_task.py --model doubao-seedance-2-0-260128 --draft-task-id cgt-xxxx
```

## References Routing

- Read `references/api-workflow.md` for API payload, status polling, parameter constraints, retention, and limits.
- Read `references/prompt-playbook.md` for prompt structure, multimodal references, and reusable prompt templates.

## Failure Handling

- Missing `ARK_API_KEY`: ask user to set env var; do not hardcode key.
- `failed` task: return full error object and likely causes (permissions/model access/invalid URL/invalid params).
- Task creation throttled: backoff and retry with reduced concurrency.
- Expired output URL: regenerate or use persistent backup.

## Sources

- https://www.volcengine.com/docs/82379/2291680?lang=zh
- https://www.volcengine.com/docs/82379/2222480?lang=zh
- https://www.volcengine.com/docs/82379/2298881?lang=zh

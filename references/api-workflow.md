# Seedance Video Generation API Workflow

## 1) Prerequisites

- Set environment variable `ARK_API_KEY`.
- Confirm model access is enabled in Volcengine Ark (account balance ≥ 200 CNY or resource pack purchased).
- Use public URLs for input media (image/video/audio). Local files can be base64-encoded for images only (≤30 MB).

## 2) Models

| Model | ID | Notes |
|---|---|---|
| Seedance 2.0 | `doubao-seedance-2-0-260128` | Highest quality; supports 1080p; online inference only |
| Seedance 2.0 fast | `doubao-seedance-2-0-fast-260128` | Lower cost, faster; max 720p; online inference only |
| Seedance 1.5 pro | `doubao-seedance-1-5-pro-251215` | Supports draft mode, offline inference, camera_fixed, heic/heif images |
| Seedance 1.0 pro | `doubao-seedance-1-0-pro-250528` | Offline inference; 2–12s duration |
| Seedance 1.0 pro fast | `doubao-seedance-1-0-pro-fast-251015` | Offline inference; 2–12s duration |
| Seedance 1.0 lite i2v | `doubao-seedance-1-0-lite-i2v-250428` | Image reference (1–4 images); offline inference; 2–12s |
| Seedance 1.0 lite t2v | `doubao-seedance-1-0-lite-t2v-250428` | Text-to-video; offline inference; 2–12s |

**Capability matrix:**

| Feature | 2.0 | 2.0 fast | 1.5 pro | 1.0 pro | 1.0 pro fast | 1.0 lite i2v | 1.0 lite t2v |
|---|---|---|---|---|---|---|---|
| Text-to-video | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Image-to-video (first frame) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — |
| Image-to-video (first+last frame) | ✓ | ✓ | ✓ | ✓ | — | ✓ | — |
| Multimodal reference (images) | ✓ | ✓ | — | — | — | ✓ | — |
| Multimodal reference (video) | ✓ | ✓ | — | — | — | — | — |
| Multimodal reference (combined) | ✓ | ✓ | — | — | — | — | — |
| Video edit | ✓ | ✓ | — | — | — | — | — |
| Video extend | ✓ | ✓ | — | — | — | — | — |
| Generate audio | ✓ | ✓ | ✓ | — | — | — | — |
| Web search tool | ✓ | ✓ | — | — | — | — | — |
| Draft mode | — | — | ✓ | — | — | — | — |
| Return last frame | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Offline inference (`flex`) | — | — | ✓ | ✓ | ✓ | ✓ | ✓ |
| `camera_fixed` | — | — | ✓ | ✓ | ✓ | ✓ (no ref) | — |
| Max resolution | 1080p | 720p | 1080p | 1080p | 720p→1080p | 1080p | 1080p |
| Duration range | 4–15s | 4–15s | 4–12s | 2–12s | 2–12s | 2–12s | 2–12s |

## 3) Async Task Pattern

Seedance video generation is asynchronous.

1. Create task: `POST /contents/generations/tasks`
2. Poll task: `GET /contents/generations/tasks/{id}`
3. Read final file URL from `content.video_url` when status is `succeeded`

Typical statuses: `queued`, `running`, `succeeded`, `failed`, `expired`.

Task metadata and generated URLs are retained for ~24 hours. Persist outputs early.

## 4) Payload Essentials

Required:
- `model`
- `content` list

Common optional fields:

| Field | Description |
|---|---|
| `generate_audio` | bool; generates audio track with the video |
| `return_last_frame` | `"true"` string; returns `content.last_frame_url` in result (useful for chaining clips) |
| `resolution` | `480p`, `720p`; `1080p` for Seedance 2.0 / 1.5 pro / 1.0 pro / 1.0 lite |
| `ratio` | `adaptive`, `16:9`, `9:16`, `1:1`, `4:3`, `3:4`, `21:9` |
| `duration` | 4–15 seconds (model-dependent); mutually exclusive with `frames` |
| `frames` | integer; supported range [29,289] matching `25+4n` pattern (1.0 pro / lite only) |
| `seed` | integer for reproducibility |
| `camera_fixed` | bool; fix the camera (not supported on 2.0 / 2.0 fast; not supported with reference image on lite) |
| `watermark` | bool; add platform watermark |
| `callback_url` | webhook URL; POST called on each status change |
| `draft` | bool; enable draft mode (1.5 pro only, 480p only) |
| `service_tier` | `"flex"` for offline/batch inference (50% cost, not available for 2.0/2.0 fast) |
| `execution_expires_after` | seconds until task auto-terminates (use with `flex` to bound max wait) |
| `tools` | array; `[{"type": "web_search"}]` enables live web search for text-only prompts |

**Strongly prefer explicit request-body fields over appending `--params` in prompt text.** The request-body method is strictly validated and returns errors on bad input; the prompt-append method silently falls back to defaults.

Rate limits (online inference):
- Enterprise: max 600 RPM, 10 concurrent tasks (2.0 / 2.0 fast)
- Personal: max 180 RPM, 3 concurrent tasks (2.0 / 2.0 fast)
- 1.0 lite models: 300 RPM, 5 concurrent tasks

## 5) Content Item Patterns

Use `content` items:

- `{"type": "text", "text": "..."}` — prompt text
- `{"type": "image_url", "image_url": {"url": "..."}, "role": "reference_image"}` — multimodal reference image
- `{"type": "video_url", "video_url": {"url": "..."}, "role": "reference_video"}` — multimodal reference / edit / extend video
- `{"type": "audio_url", "audio_url": {"url": "..."}, "role": "reference_audio"}` — audio reference (timbre, music, dialogue)
- For strict frame lock: `"role": "first_frame"` or `"role": "last_frame"` on image items
- For draft-to-final: `{"type": "draft_task", "draft_task": {"id": "cgt-..."}}`

**Multimodal combination limits:**
- Images: 0–9 per request (Seedance 2.0); 1–4 for Seedance 1.0 lite i2v reference
- Videos: 0–3 per request
- Audios: 0–3 per request
- Unsupported combinations: text+audio only, audio-only

**Referencing in prompt:** Use ordinal tokens by modality upload order — `图片1`, `图片2`, `视频1`, `音频1`. For example: `[图1]中的男生和[图2]的小狗坐在[图3]的草坪上`.

## 6) Input Media Requirements

### Images
- **Formats:** jpeg, png, webp, bmp, tiff, gif (1.5 pro also supports heic, heif)
- **Aspect ratio (W/H):** 0.4 to 2.5
- **Dimensions:** 300–6000 px per side
- **Size:** ≤30 MB per image; request body ≤64 MB (avoid base64 for large files)
- **Count:** first-frame: 1; first+last frame: 2; 2.0 multimodal: 1–9; 1.0 lite ref: 1–4

### Videos
- **Formats:** mp4 (H.264/H.265, AAC/MP3), mov (H.264/H.265, AAC/MP3)
- **Resolution:** 480p, 720p, 1080p
- **Duration:** 2–15 s per clip; max 3 clips; total ≤15 s
- **Aspect ratio (W/H):** 0.4 to 2.5
- **Dimensions:** 300–6000 px per side
- **Total pixels:** 409,600–2,086,876 (640×640 to 2206×946)
- **Size:** ≤50 MB per video
- **FPS:** 24–60

### Audio
- **Formats:** wav, mp3
- **Duration:** 2–15 s per clip; max 3 clips; total ≤15 s
- **Size:** ≤15 MB per audio; request body ≤64 MB

## 7) Asset URLs (Virtual Avatars & Authorized Real Portraits)

Platform pre-built virtual avatars and authorized real-person assets use the `asset://` URL scheme:

```
"image_url": {"url": "asset://<asset-id>"}
```

Asset ID format example: `asset-20260401123823-6d4x2`. Obtain IDs from the Ark console virtual avatar library or by registering real-person assets. In prompts, still refer to assets by ordinal (`图片1`, not the asset ID).

## 8) Trusted Model Outputs (Face Re-use Policy)

Seedance 2.0 blocks direct upload of reference images/videos containing real human faces. The following platform-generated outputs are trusted for secondary creation within 30 days of generation (same account only):

- Seedance 2.0 / 2.0 fast generated videos with faces (effective 2026-03-11)
- Last-frame images from Seedance 2.0 / 2.0 fast face videos (effective 2026-04-16)
- Seedream 5.0 lite text-to-image outputs with faces (effective 2026-04-16)

Only unedited original outputs qualify; edited versions or outputs older than 30 days do not.

## 9) Web Search Tool

Enable by adding `tools=[{"type": "web_search"}]` to the request. Only works with pure text input (no image/video/audio). The model autonomously decides whether to search. Real search count is in `usage.tool_usage.web_search` in the response (0 = no search performed).

## 10) Video Edit Task

Pass the source video as `reference_video`, optionally add reference images/audio, and describe the edit in the prompt. Supports: element add/remove/replace, regional repaint/repair.

## 11) Video Extend Task

Pass 1–3 videos as `reference_video` items to:
- Extend a single video forward or backward
- Connect 2–3 video clips with generated transitions (total output ≤15 s)

The model automatically clips the join segments; original video content is included in output.

## 12) Draft Mode (Seedance 1.5 pro only)

Draft mode generates a low-cost preview video to validate scene structure, camera scheduling, and subject motion before committing to a full render.

**Step 1 — Create draft task:**
- Set `"draft": true` in the request
- Only 480p resolution supported (other resolutions cause an error)
- `return_last_frame` and `service_tier: flex` are not supported in draft mode
- Draft token cost = normal token cost × 0.6 (for audio video)

**Step 2 — Promote draft to final video:**
- Use `{"type": "draft_task", "draft_task": {"id": "cgt-..."}}` as the content item
- Platform automatically reuses: model, content.text, content.image_url, generate_audio, seed, ratio, duration, camera_fixed from the draft
- You can override: resolution, watermark, service_tier, return_last_frame
- Draft task IDs are valid for 7 days from creation

## 13) Chaining Clips (Sequential Video Generation)

Use `return_last_frame=True` to get `content.last_frame_url` from a completed task, then pass that URL as the `first_frame` image in the next task. This lets you chain multiple short clips into a longer narrative. Concatenate the resulting MP4s with FFmpeg.

## 14) Webhook Notifications

Set `callback_url` in the request. Ark sends a POST to that URL on each status change. The request body matches the GET task response structure:

```json
{
  "id": "cgt-2025****",
  "model": "doubao-seedance-2-0-260128",
  "status": "running",
  "created_at": 1765434920,
  "updated_at": 1765434920,
  "service_tier": "default",
  "execution_expires_after": 172800
}
```

Your webhook endpoint must be publicly accessible and return a 2xx response.

## 15) Task Management APIs

- **List tasks:** `GET /contents/generations/tasks?page_size=N&filter.status=succeeded`
- **Delete/cancel task:** `DELETE /contents/generations/tasks/{id}` — cancels queued tasks or deletes task records

## 16) Image Cropping (Image-to-Video)

When target `ratio` differs from the uploaded image's aspect ratio, Ark center-crops the image:

- If original ratio < target ratio (image is "too tall"): crop based on width. `crop_h = (B/A) × W`
- If original ratio > target ratio (image is "too wide"): crop based on height. `crop_w = (A/B) × H`
- Cropping is always centered

**Best practice:** choose a `ratio` that matches your input image's native aspect ratio to avoid unintended cropping.

## 17) Offline Inference (`service_tier: flex`)

Not supported on Seedance 2.0 / 2.0 fast.

For latency-insensitive workloads (e.g., hour-level turnaround), set `service_tier="flex"` to use offline inference at 50% of online pricing. Set `execution_expires_after` (in seconds) to bound how long a task can run before auto-terminating. The default is 172800 (48 hours).

## 18) Prompt Guidelines

- Structure: `subject + motion, background + motion, camera + motion`
- Use concrete, specific descriptions rather than abstract ones
- For precise visual output: generate an image with a text-to-image model first, then use image-to-video
- Text-to-video has high randomness — good for inspiration; image-to-video gives more control
- Upload high-quality, high-resolution images for image-to-video
- Move important content to the front of the prompt

## 19) Operational Guardrails

- Task metadata and generated URLs are retained for ~24 hours; persist outputs early (recommend TOS data subscription for auto-archival)
- Image-to-video triggers center-crop when input ratio differs from target ratio
- Single image ≤30 MB, single video ≤50 MB, single audio ≤15 MB; request body ≤64 MB
- Use URL-based upload for large inputs instead of base64 inline blobs
- If throttled (RPM/concurrency), back off and retry
- flex TPD daily limit: 500 billion tokens for 1.5 pro / 1.0 pro; 250 billion for 1.0 lite

## 20) Helper Script

Use `scripts/run_seedance_task.py` to standardize:

- request construction
- task creation
- polling and timeout control
- JSON output persistence

## Sources

- https://www.volcengine.com/docs/82379/2291680?lang=zh
- https://www.volcengine.com/docs/82379/2298881?lang=zh

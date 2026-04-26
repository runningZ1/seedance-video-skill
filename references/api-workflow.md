# Seedance 2.0 API Workflow

## 1) Prerequisites

- Set environment variable `ARK_API_KEY`.
- Confirm model access is enabled in Volcengine Ark (account balance ≥ 200 CNY or resource pack purchased).
- Use public URLs for input media (image/video/audio).

## 2) Models

| Model | ID | Notes |
|---|---|---|
| Seedance 2.0 | `doubao-seedance-2-0-260128` | Highest quality; supports 1080p |
| Seedance 2.0 fast | `doubao-seedance-2-0-fast-260128` | Lower cost, faster; max 720p |

Both models support: text-to-video, image-to-video (first frame / first+last frame), multimodal reference, video edit, video extend, web search, generate audio, return last frame.

## 3) Async Task Pattern

Seedance video generation is asynchronous.

1. Create task: `POST /contents/generations/tasks`
2. Poll task: `GET /contents/generations/tasks/{id}`
3. Read final file URL from `content.video_url` when status is `succeeded`

Typical statuses: `queued`, `running`, `succeeded`, `failed`, `expired`.

## 4) Payload Essentials

Required:

- `model`
- `content` list

Common optional fields:

- `generate_audio` — bool, generates audio track with the video
- `return_last_frame` — `"true"` string; returns `content.last_frame_url` in result (useful for chaining)
- `resolution` (`480p`, `720p`; `1080p` for Seedance 2.0 only)
- `ratio` (`adaptive`, `16:9`, `9:16`, `1:1`, `4:3`, `3:4`, `21:9`)
- `duration` (4–15 seconds) or `frames`
- `seed`
- `camera_fixed`
- `watermark`
- `callback_url` (webhook)
- `service_tier` — set to `"flex"` for offline/batch inference (lower cost, not real-time)
- `tools` — array; `[{"type": "web_search"}]` enables live web search for text-only prompts

Prefer explicit request-body fields over appending `--params` in prompt text.

Rate limits (online inference):
- Enterprise: max 600 RPM, 10 concurrent tasks
- Personal: max 180 RPM, 3 concurrent tasks

## 5) Content Item Patterns

Use `content` items:

- `{"type": "text", "text": "..."}` — prompt text
- `{"type": "image_url", "image_url": {"url": "..."}, "role": "reference_image"}` — multimodal reference image
- `{"type": "video_url", "video_url": {"url": "..."}, "role": "reference_video"}` — multimodal reference / edit / extend video
- `{"type": "audio_url", "audio_url": {"url": "..."}, "role": "reference_audio"}` — audio reference (timbre, music, dialogue)
- For strict frame lock: `"role": "first_frame"` or `"role": "last_frame"` on image items
- For draft-to-final: `{"type": "draft_task", "draft_task": {"id": "cgt-..."}}`

**Multimodal combination limits:**
- Images: 0–9 per request
- Videos: 0–3 per request
- Audios: 0–3 per request
- Unsupported combinations: text+audio only, audio-only

**Referencing in prompt:** Use ordinal tokens by modality upload order — `图片1`, `图片2`, `视频1`, `音频1`.

## 6) Asset URLs (Virtual Avatars & Authorized Real Portraits)

Platform pre-built virtual avatars and authorized real-person assets use the `asset://` URL scheme:

```
"image_url": {"url": "asset://<asset-id>"}
```

Asset ID format example: `asset-20260401123823-6d4x2`. Obtain IDs from the Ark console virtual avatar library or by registering real-person assets. In prompts, still refer to assets by ordinal (`图片1`, not the asset ID).

## 7) Trusted Model Outputs (Face Re-use Policy)

Seedance 2.0 blocks direct upload of reference images/videos containing real human faces. The following platform-generated outputs are trusted for secondary creation within 30 days of generation (same account only):

- Seedance 2.0 / 2.0 fast generated videos with faces (effective 2026-03-11)
- Last-frame images from Seedance 2.0 / 2.0 fast face videos (effective 2026-04-16)
- Seedream 5.0 lite text-to-image outputs with faces (effective 2026-04-16)

Only unedited original outputs qualify; edited versions or outputs older than 30 days do not.

## 8) Web Search Tool

Enable by adding `tools=[{"type": "web_search"}]` to the request. Only works with pure text input (no image/video/audio). The model autonomously decides whether to search. Real search count is in `usage.tool_usage.web_search` in the response (0 = no search performed).

## 9) Video Edit Task

Pass the source video as `reference_video`, optionally add reference images/audio, and describe the edit in the prompt. Supports: element add/remove/replace, regional repaint/repair.

## 10) Video Extend Task

Pass 1–3 videos as `reference_video` items to:
- Extend a single video forward or backward
- Connect 2–3 video clips with generated transitions (total output ≤ 15 s)

The model automatically clips the join segments; original video content is included in output.

## 11) Operational Guardrails

- Task metadata and generated URLs are retained for around 24 hours; persist outputs early (recommend TOS data subscription for auto-archival).
- Image-to-video can trigger center-crop when input ratio differs from target ratio.
- Single image size should stay under 30MB; request body should stay under 64MB.
- Large inputs should use URL-based upload, not base64 inline blobs.
- If throttled (RPM/concurrency), back off and retry.

## 12) Helper Script

Use `scripts/run_seedance_task.py` to standardize:

- request construction
- task creation
- polling and timeout control
- JSON output persistence

## Sources

- https://www.volcengine.com/docs/82379/2291680?lang=zh
- https://www.volcengine.com/docs/82379/2298881?lang=zh

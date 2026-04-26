#!/usr/bin/env python3
"""Create and poll Seedance video generation tasks with a single command."""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import sys
import time
from pathlib import Path
from typing import Any


def parse_bool(raw: str) -> bool:
    value = raw.strip().lower()
    truthy = {"1", "true", "t", "yes", "y", "on"}
    falsy = {"0", "false", "f", "no", "n", "off"}
    if value in truthy:
        return True
    if value in falsy:
        return False
    raise argparse.ArgumentTypeError(f"Invalid boolean value: {raw}")


MAX_IMAGE_BYTES = 30 * 1024 * 1024
ALLOWED_IMAGE_MIME = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/bmp",
    "image/tiff",
    "image/gif",
    "image/heic",
    "image/heif",
}


def load_env_file(env_file: Path) -> None:
    if not env_file.exists():
        return

    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1]
        os.environ.setdefault(key, value)


def to_plain(data: Any) -> Any:
    if data is None or isinstance(data, (str, int, float, bool)):
        return data
    if isinstance(data, list):
        return [to_plain(item) for item in data]
    if isinstance(data, tuple):
        return [to_plain(item) for item in data]
    if isinstance(data, dict):
        return {str(key): to_plain(value) for key, value in data.items()}

    for method_name in ("model_dump", "to_dict", "dict"):
        method = getattr(data, method_name, None)
        if callable(method):
            try:
                return to_plain(method())
            except TypeError:
                pass

    if hasattr(data, "__dict__"):
        return to_plain(vars(data))
    return str(data)


def summarize_for_log(data: Any) -> Any:
    if isinstance(data, dict):
        result: dict[str, Any] = {}
        for key, value in data.items():
            if key == "url" and isinstance(value, str) and value.startswith("data:image/"):
                mime = value.split(";", 1)[0].replace("data:", "")
                result[key] = f"<base64:{mime}, chars={len(value)}>"
            else:
                result[key] = summarize_for_log(value)
        return result
    if isinstance(data, list):
        return [summarize_for_log(item) for item in data]
    if isinstance(data, str) and len(data) > 500:
        return f"<string chars={len(data)}>"
    return data


def get_field(obj: Any, key: str, default: Any = None) -> Any:
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def append_urls(
    content: list[dict[str, Any]],
    urls: list[str],
    item_type: str,
    role: str,
) -> None:
    for url in urls:
        item: dict[str, Any] = {"type": item_type, role_to_key(item_type): {"url": url}}
        if role:
            item["role"] = role
        content.append(item)


def local_image_to_data_uri(raw_path: str) -> str:
    path = Path(raw_path).expanduser().resolve()
    if not path.exists() or not path.is_file():
        raise ValueError(f"Image file does not exist: {raw_path}")

    file_size = path.stat().st_size
    if file_size > MAX_IMAGE_BYTES:
        raise ValueError(
            f"Image file exceeds 30MB limit ({file_size} bytes): {raw_path}"
        )

    mime_type, _ = mimetypes.guess_type(path.name)
    if not mime_type or mime_type not in ALLOWED_IMAGE_MIME:
        raise ValueError(
            f"Unsupported image format for local upload: {raw_path}. "
            "Use jpeg/png/webp/bmp/tiff/gif (heic/heif model-dependent)."
        )

    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def merge_image_sources(urls: list[str], files: list[str]) -> list[str]:
    merged = list(urls)
    for file_path in files:
        merged.append(local_image_to_data_uri(file_path))
    return merged


def looks_like_local_path(raw: str) -> bool:
    value = raw.strip()
    if not value:
        return False
    if value.startswith("file://"):
        return True
    if value.startswith("./") or value.startswith("../"):
        return True
    if len(value) >= 2 and value[1] == ":":
        return True
    if value.startswith("\\\\"):
        return True
    path = Path(value)
    return path.exists()


def ensure_not_local_path(values: list[str], flag_name: str) -> None:
    for value in values:
        if looks_like_local_path(value):
            raise ValueError(
                f"{flag_name} does not support local files: {value}. "
                "Use a public URL."
            )


def role_to_key(item_type: str) -> str:
    if item_type == "image_url":
        return "image_url"
    if item_type == "video_url":
        return "video_url"
    if item_type == "audio_url":
        return "audio_url"
    raise ValueError(f"Unsupported item type: {item_type}")


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.frames is not None and args.duration is not None:
        raise ValueError("Use either --duration or --frames, not both.")

    payload: dict[str, Any] = {"model": args.model}
    content: list[dict[str, Any]] = []

    if args.draft_task_id:
        content.append(
            {
                "type": "draft_task",
                "draft_task": {"id": args.draft_task_id},
            }
        )
    else:
        if not args.prompt:
            raise ValueError("--prompt is required unless --draft-task-id is provided.")

        content.append({"type": "text", "text": args.prompt})
        ref_images = merge_image_sources(args.image_url, args.image_file)
        first_frames = merge_image_sources(args.first_frame_url, args.first_frame_file)
        last_frames = merge_image_sources(args.last_frame_url, args.last_frame_file)
        ensure_not_local_path(args.video_url, "--video-url")
        ensure_not_local_path(args.audio_url, "--audio-url")

        append_urls(content, ref_images, "image_url", "reference_image")
        append_urls(content, args.video_url, "video_url", "reference_video")
        append_urls(content, args.audio_url, "audio_url", "reference_audio")
        append_urls(content, first_frames, "image_url", "first_frame")
        append_urls(content, last_frames, "image_url", "last_frame")

    payload["content"] = content

    if args.callback_url:
        payload["callback_url"] = args.callback_url
    if args.draft:
        payload["draft"] = True
    if args.web_search:
        payload["tools"] = [{"type": "web_search"}]
    if args.return_last_frame:
        payload["return_last_frame"] = "true"
    if args.service_tier:
        payload["service_tier"] = args.service_tier
    if args.execution_expires_after is not None:
        payload["execution_expires_after"] = args.execution_expires_after

    # For non-draft-task flow, set practical defaults.
    if not args.draft_task_id:
        payload["generate_audio"] = True if args.generate_audio is None else args.generate_audio
        payload["ratio"] = args.ratio or "adaptive"
        if args.frames is None and args.duration is None:
            payload["duration"] = 5

    optional_fields = (
        "resolution",
        "ratio",
        "duration",
        "frames",
        "seed",
        "camera_fixed",
        "watermark",
        "generate_audio",
    )
    for field in optional_fields:
        value = getattr(args, field)
        if value is not None:
            payload[field] = value

    return payload


def wait_for_terminal_status(
    client: Any,
    task_id: str,
    poll_interval: float,
    timeout_seconds: int,
) -> tuple[str, Any]:
    deadline = time.time() + timeout_seconds if timeout_seconds > 0 else None

    while True:
        result = client.content_generation.tasks.get(task_id=task_id)
        status = (get_field(result, "status") or "").lower()
        print(f"Task {task_id} status: {status or 'unknown'}")

        if status in {"succeeded", "failed", "expired"}:
            return status, result

        if deadline is not None and time.time() >= deadline:
            raise TimeoutError(
                f"Polling timeout after {timeout_seconds}s, last status={status or 'unknown'}"
            )

        time.sleep(poll_interval)


def write_json(path: str, data: Any) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(to_plain(data), ensure_ascii=False, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create and poll Volcengine Seedance video generation tasks."
    )
    parser.add_argument(
        "--model",
        default=os.environ.get("SEEDANCE_MODEL_DEFAULT", "doubao-seedance-2-0-260128"),
    )
    parser.add_argument("--prompt")
    parser.add_argument("--image-url", action="append", default=[])
    parser.add_argument(
        "--image-file",
        action="append",
        default=[],
        help="Local image file path. Will be encoded to base64 image data.",
    )
    parser.add_argument("--video-url", action="append", default=[])
    parser.add_argument("--audio-url", action="append", default=[])
    parser.add_argument("--first-frame-url", action="append", default=[])
    parser.add_argument(
        "--first-frame-file",
        action="append",
        default=[],
        help="Local first-frame image file path. Encoded to base64 image data.",
    )
    parser.add_argument("--last-frame-url", action="append", default=[])
    parser.add_argument(
        "--last-frame-file",
        action="append",
        default=[],
        help="Local last-frame image file path. Encoded to base64 image data.",
    )
    parser.add_argument("--draft-task-id")

    parser.add_argument("--generate-audio", type=parse_bool)
    parser.add_argument("--resolution")
    parser.add_argument("--ratio")
    parser.add_argument("--duration", type=int)
    parser.add_argument("--frames", type=int)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--camera-fixed", type=parse_bool, dest="camera_fixed")
    parser.add_argument("--watermark", type=parse_bool)
    parser.add_argument("--callback-url")
    parser.add_argument("--draft", action="store_true")
    parser.add_argument(
        "--web-search",
        action="store_true",
        help="Enable web search tool (text-only input only). Adds tools=[{type:web_search}].",
    )
    parser.add_argument(
        "--return-last-frame",
        type=parse_bool,
        dest="return_last_frame",
        help="Return the last frame image URL of the generated video.",
    )
    parser.add_argument(
        "--service-tier",
        dest="service_tier",
        help='Set to "flex" for offline/batch inference (50%% cost; not available for 2.0/2.0-fast).',
    )
    parser.add_argument(
        "--execution-expires-after",
        type=int,
        dest="execution_expires_after",
        help="Seconds until task auto-terminates (use with --service-tier flex). Default: 172800 (48h).",
    )

    parser.add_argument("--poll-interval", type=float, default=15.0)
    parser.add_argument("--timeout", type=int, default=1800)
    parser.add_argument("--no-poll", action="store_true")
    parser.add_argument("--output-json")
    return parser.parse_args()


def main() -> int:
    env_path = Path(__file__).resolve().parents[1] / ".env"
    load_env_file(env_path)

    args = parse_args()

    if args.poll_interval <= 0:
        print("--poll-interval must be > 0", file=sys.stderr)
        return 2
    if args.duration is not None and args.duration <= 0:
        print("--duration must be > 0", file=sys.stderr)
        return 2
    if args.frames is not None and args.frames <= 0:
        print("--frames must be > 0", file=sys.stderr)
        return 2
    if args.image_file and args.image_url:
        print(
            "Both --image-url and --image-file are set. "
            "Reference order will be URLs first, then local files.",
            file=sys.stderr,
        )
    if args.first_frame_file and args.first_frame_url:
        print(
            "Both --first-frame-url and --first-frame-file are set. "
            "Order will be URLs first, then local files.",
            file=sys.stderr,
        )
    if args.last_frame_file and args.last_frame_url:
        print(
            "Both --last-frame-url and --last-frame-file are set. "
            "Order will be URLs first, then local files.",
            file=sys.stderr,
        )

    api_key = os.environ.get("ARK_API_KEY")
    if not api_key:
        print("ARK_API_KEY is missing in environment.", file=sys.stderr)
        return 2

    try:
        payload = build_payload(args)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    try:
        from volcenginesdkarkruntime import Ark
    except ImportError:
        print(
            "Missing dependency: volcenginesdkarkruntime. Install it first.",
            file=sys.stderr,
        )
        return 2

    client = Ark(api_key=api_key)
    print("Creating task with payload:")
    print(json.dumps(summarize_for_log(to_plain(payload)), ensure_ascii=False, indent=2))

    create_result = client.content_generation.tasks.create(**payload)
    task_id = get_field(create_result, "id")
    if not task_id:
        plain = to_plain(create_result)
        task_id = plain.get("id") if isinstance(plain, dict) else None
    if not task_id:
        print("Task creation succeeded but response missing id.", file=sys.stderr)
        if args.output_json:
            write_json(args.output_json, {"create_result": create_result})
        return 2

    print(f"Task created: {task_id}")

    output: dict[str, Any] = {"payload": payload, "create_result": create_result}
    if args.no_poll:
        if args.output_json:
            write_json(args.output_json, output)
        return 0

    try:
        final_status, final_result = wait_for_terminal_status(
            client=client,
            task_id=task_id,
            poll_interval=args.poll_interval,
            timeout_seconds=args.timeout,
        )
    except TimeoutError as exc:
        print(str(exc), file=sys.stderr)
        output["timeout"] = str(exc)
        if args.output_json:
            write_json(args.output_json, output)
        return 3

    output["final_status"] = final_status
    output["final_result"] = final_result

    plain_final = to_plain(final_result)
    content = plain_final.get("content") if isinstance(plain_final, dict) else None
    video_url = content.get("video_url") if isinstance(content, dict) else None
    last_frame_url = content.get("last_frame_url") if isinstance(content, dict) else None

    if video_url:
        print(f"Video URL: {video_url}")
    if last_frame_url:
        print(f"Last frame URL: {last_frame_url}")
    if final_status == "failed":
        error_obj = plain_final.get("error") if isinstance(plain_final, dict) else None
        print(f"Task failed: {json.dumps(error_obj, ensure_ascii=False)}", file=sys.stderr)
    elif final_status == "expired":
        print("Task expired before retrieval.", file=sys.stderr)

    if args.output_json:
        write_json(args.output_json, output)

    return 0 if final_status == "succeeded" else 4


if __name__ == "__main__":
    sys.exit(main())

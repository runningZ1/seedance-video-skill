#!/usr/bin/env python3
"""Create and poll Seedance image-to-video tasks."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from run_seedance_task import (
    build_payload,
    get_field,
    load_env_file,
    parse_bool,
    summarize_for_log,
    to_plain,
    wait_for_terminal_status,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create and poll Seedance image-to-video generation tasks."
    )
    parser.add_argument(
        "--model",
        default=os.environ.get("SEEDANCE_MODEL_DEFAULT", "doubao-seedance-2-0-260128"),
        help="Seedance model id.",
    )
    parser.add_argument("--prompt", required=True, help="Video generation prompt.")
    parser.add_argument("--image-url", action="append", default=[], help="Public image URL.")
    parser.add_argument(
        "--image-file",
        action="append",
        default=[],
        help="Local image path. The script encodes it to base64 data URI.",
    )

    parser.add_argument("--resolution")
    parser.add_argument("--ratio", default="adaptive")
    parser.add_argument("--duration", type=int, default=5)
    parser.add_argument("--frames", type=int)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--camera-fixed", type=parse_bool, dest="camera_fixed")
    parser.add_argument("--watermark", type=parse_bool)
    parser.add_argument(
        "--generate-audio",
        type=parse_bool,
        default=False,
        help="Enable generated audio. Default false for image-to-video.",
    )
    parser.add_argument("--callback-url")

    parser.add_argument("--poll-interval", type=float, default=15.0)
    parser.add_argument("--timeout", type=int, default=1800)
    parser.add_argument("--no-poll", action="store_true")
    parser.add_argument("--output-json")
    return parser.parse_args()


def to_seedance_namespace(args: argparse.Namespace) -> SimpleNamespace:
    return SimpleNamespace(
        model=args.model,
        prompt=args.prompt,
        image_url=args.image_url,
        image_file=args.image_file,
        video_url=[],
        audio_url=[],
        first_frame_url=[],
        first_frame_file=[],
        last_frame_url=[],
        last_frame_file=[],
        draft_task_id=None,
        generate_audio=args.generate_audio,
        resolution=args.resolution,
        ratio=args.ratio,
        duration=args.duration,
        frames=args.frames,
        seed=args.seed,
        camera_fixed=args.camera_fixed,
        watermark=args.watermark,
        callback_url=args.callback_url,
        draft=False,
    )


def main() -> int:
    env_path = Path(__file__).resolve().parents[1] / ".env"
    load_env_file(env_path)
    args = parse_args()

    if not args.image_url and not args.image_file:
        print("At least one --image-url or --image-file is required.", file=sys.stderr)
        return 2
    if args.poll_interval <= 0:
        print("--poll-interval must be > 0", file=sys.stderr)
        return 2
    if args.duration is not None and args.duration <= 0:
        print("--duration must be > 0", file=sys.stderr)
        return 2
    if args.frames is not None and args.frames <= 0:
        print("--frames must be > 0", file=sys.stderr)
        return 2

    api_key = os.environ.get("ARK_API_KEY")
    if not api_key:
        print("ARK_API_KEY is missing in environment.", file=sys.stderr)
        return 2

    try:
        payload = build_payload(to_seedance_namespace(args))
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
    print("Creating image-to-video task with payload:")
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
        return 3

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
        return 4

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

    return 0 if final_status == "succeeded" else 5


if __name__ == "__main__":
    sys.exit(main())

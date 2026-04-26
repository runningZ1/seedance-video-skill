#!/usr/bin/env python3
"""Create and poll Duomi NANO-BANANA text-to-image tasks."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any
from urllib import error, request


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


def parse_json_field(raw: str) -> dict[str, Any]:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise argparse.ArgumentTypeError(f"--extra-json is not valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise argparse.ArgumentTypeError("--extra-json must be a JSON object")
    return data


def to_plain(data: Any) -> Any:
    if data is None or isinstance(data, (str, int, float, bool)):
        return data
    if isinstance(data, list):
        return [to_plain(item) for item in data]
    if isinstance(data, tuple):
        return [to_plain(item) for item in data]
    if isinstance(data, dict):
        return {str(key): to_plain(value) for key, value in data.items()}
    return str(data)


def request_json(
    method: str,
    url: str,
    headers: dict[str, str],
    timeout: int,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    data_bytes = None
    if payload is not None:
        data_bytes = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    req = request.Request(url=url, method=method.upper(), data=data_bytes)
    for key, value in headers.items():
        req.add_header(key, value)

    try:
        with request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"HTTP {exc.code} calling {url}: {body or exc.reason}"
        ) from exc
    except error.URLError as exc:
        raise RuntimeError(f"Network error calling {url}: {exc.reason}") from exc

    if not raw.strip():
        return {}

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON response from {url}: {raw}") from exc
    if not isinstance(parsed, dict):
        raise RuntimeError(f"Unexpected response type from {url}: {type(parsed).__name__}")
    return parsed


def build_create_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": args.model,
        "prompt": args.prompt,
        "aspect_ratio": args.aspect_ratio,
        "image_size": args.image_size,
    }
    if args.extra_json:
        payload.update(args.extra_json)
    return payload


def extract_task_id(create_result: dict[str, Any]) -> str | None:
    data = create_result.get("data")
    if isinstance(data, dict):
        task_id = data.get("task_id")
        if isinstance(task_id, str) and task_id.strip():
            return task_id.strip()
    return None


def api_code_ok(result: dict[str, Any]) -> bool:
    code = result.get("code")
    if code is None:
        return True
    return str(code) == "200"


def api_error_text(result: dict[str, Any]) -> str:
    msg = result.get("msg")
    if isinstance(msg, str) and msg.strip():
        return msg.strip()
    return json.dumps(result, ensure_ascii=False)


def get_state_and_status(query_result: dict[str, Any]) -> tuple[str, str]:
    data = query_result.get("data")
    if not isinstance(data, dict):
        return "", ""

    raw_state = data.get("state")
    raw_status = data.get("status")

    state = str(raw_state).strip().lower() if raw_state is not None else ""
    status = str(raw_status).strip() if raw_status is not None else ""
    return state, status


def is_succeeded(state: str, status: str) -> bool:
    if state in {"succeeded", "success", "completed", "done"}:
        return True
    return status in {"3"}


def is_failed(state: str, status: str) -> bool:
    if state in {"failed", "error", "canceled", "cancelled", "expired", "timeout"}:
        return True
    return status in {"2", "4", "5", "-1"}


def extract_image_urls(query_result: dict[str, Any]) -> list[str]:
    data = query_result.get("data")
    if not isinstance(data, dict):
        return []
    result = data.get("data")
    if not isinstance(result, dict):
        return []
    images = result.get("images")
    if not isinstance(images, list):
        return []

    urls: list[str] = []
    for item in images:
        if isinstance(item, dict):
            url = item.get("url")
            if isinstance(url, str) and url.strip():
                urls.append(url.strip())
    return urls


def extract_task_message(query_result: dict[str, Any]) -> str:
    data = query_result.get("data")
    if not isinstance(data, dict):
        return ""
    msg = data.get("msg")
    if isinstance(msg, str):
        return msg.strip()
    return ""


def write_json(path: str, payload: Any) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(to_plain(payload), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create and poll Duomi text-to-image tasks.")
    parser.add_argument("--base-url", default=os.environ.get("DUOMI_BASE_URL", "https://duomiapi.com"))
    parser.add_argument("--api-key", default=os.environ.get("DUOMI_API_KEY"))
    parser.add_argument("--model", default=os.environ.get("DUOMI_NANO_BANANA_MODEL", "gemini-3-pro-image-preview"))
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--aspect-ratio", default="")
    parser.add_argument("--image-size", default="1K")
    parser.add_argument(
        "--extra-json",
        type=parse_json_field,
        help="Extra JSON object merged into create payload, e.g. '{\"foo\":\"bar\"}'.",
    )
    parser.add_argument("--request-timeout", type=int, default=60)
    parser.add_argument("--poll-interval", type=float, default=3.0)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--no-poll", action="store_true")
    parser.add_argument("--output-json")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    env_path = Path(__file__).resolve().parents[1] / ".env"
    load_env_file(env_path)
    args = parse_args(argv)

    if not args.api_key:
        print("DUOMI_API_KEY is missing (or pass --api-key).", file=sys.stderr)
        return 2
    if args.poll_interval <= 0:
        print("--poll-interval must be > 0", file=sys.stderr)
        return 2
    if args.timeout <= 0:
        print("--timeout must be > 0", file=sys.stderr)
        return 2

    base_url = args.base_url.rstrip("/")
    create_url = f"{base_url}/api/gemini/nano-banana"

    headers = {
        "Authorization": args.api_key,
        "Content-Type": "application/json",
    }

    create_payload = build_create_payload(args)
    print("Creating task with payload:")
    print(json.dumps(create_payload, ensure_ascii=False, indent=2))

    try:
        create_result = request_json(
            method="POST",
            url=create_url,
            headers=headers,
            timeout=args.request_timeout,
            payload=create_payload,
        )
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 3

    if not api_code_ok(create_result):
        print(f"Create task failed: {api_error_text(create_result)}", file=sys.stderr)
        if args.output_json:
            write_json(args.output_json, {"create_payload": create_payload, "create_result": create_result})
        return 3

    task_id = extract_task_id(create_result)
    if not task_id:
        print("Task creation response missing data.task_id", file=sys.stderr)
        if args.output_json:
            write_json(args.output_json, {"create_payload": create_payload, "create_result": create_result})
        return 3

    print(f"Task created: {task_id}")
    output: dict[str, Any] = {
        "create_payload": create_payload,
        "create_result": create_result,
        "task_id": task_id,
    }

    if args.no_poll:
        if args.output_json:
            write_json(args.output_json, output)
        return 0

    query_url = f"{create_url}/{task_id}"
    deadline = time.time() + args.timeout
    last_result: dict[str, Any] | None = None

    while True:
        try:
            query_result = request_json(
                method="GET",
                url=query_url,
                headers={"Authorization": args.api_key},
                timeout=args.request_timeout,
            )
        except RuntimeError as exc:
            print(str(exc), file=sys.stderr)
            if args.output_json:
                output["poll_error"] = str(exc)
                if last_result is not None:
                    output["last_query_result"] = last_result
                write_json(args.output_json, output)
            return 3

        last_result = query_result
        if not api_code_ok(query_result):
            output["final_status"] = "query_error"
            output["query_result"] = query_result
            print(f"Query task failed: {api_error_text(query_result)}", file=sys.stderr)
            if args.output_json:
                write_json(args.output_json, output)
            return 4
        state, status = get_state_and_status(query_result)
        shown_state = state or "unknown"
        shown_status = status or "unknown"
        print(f"Task {task_id} state={shown_state}, status={shown_status}")

        if is_succeeded(state, status):
            image_urls = extract_image_urls(query_result)
            output["final_status"] = "succeeded"
            output["query_result"] = query_result
            output["image_urls"] = image_urls
            if image_urls:
                print("Image URLs:")
                for url in image_urls:
                    print(url)
            else:
                print("Task succeeded but no image URLs found in response.", file=sys.stderr)
            if args.output_json:
                write_json(args.output_json, output)
            return 0

        if is_failed(state, status):
            output["final_status"] = "failed"
            output["query_result"] = query_result
            detail = extract_task_message(query_result)
            if detail:
                print(f"Task failed: {detail}", file=sys.stderr)
            else:
                print("Task failed.", file=sys.stderr)
            if args.output_json:
                write_json(args.output_json, output)
            return 4

        if time.time() >= deadline:
            output["final_status"] = "timeout"
            output["last_query_result"] = query_result
            print(f"Polling timed out after {args.timeout}s", file=sys.stderr)
            if args.output_json:
                write_json(args.output_json, output)
            return 5

        time.sleep(args.poll_interval)


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Unified CLI entrypoint for Seedance and related image pipelines."""

from __future__ import annotations

import argparse
import sys
from typing import Callable

import run_duomi_nano_banana_text2img
import run_seedance_image_to_video
import run_seedance_task


Runner = Callable[[list[str] | None], int]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="seedance",
        description="Unified CLI for Seedance video generation and Duomi text-to-image.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="seedance-cli 1.0",
    )

    subparsers = parser.add_subparsers(dest="command")

    video_parser = subparsers.add_parser("video", help="Seedance video workflows")
    video_sub = video_parser.add_subparsers(dest="video_command")
    video_sub.add_parser(
        "run",
        help="General Seedance task flow (maps to run_seedance_task.py)",
    )
    video_sub.add_parser(
        "i2v",
        help="Image-to-video quick flow (maps to run_seedance_image_to_video.py)",
    )

    image_parser = subparsers.add_parser("image", help="Image generation workflows")
    image_sub = image_parser.add_subparsers(dest="image_command")
    image_sub.add_parser(
        "t2i",
        help="Duomi Nano Banana text-to-image (maps to run_duomi_nano_banana_text2img.py)",
    )

    subparsers.add_parser("task", help="Alias of: video run")
    subparsers.add_parser("i2v", help="Alias of: video i2v")
    subparsers.add_parser("duomi", help="Alias of: image t2i")

    return parser


def dispatch(argv: list[str]) -> tuple[Runner | None, list[str]]:
    if not argv:
        return run_seedance_task.main, []

    first = argv[0]
    if first.startswith("-"):
        return run_seedance_task.main, argv

    if first == "task":
        return run_seedance_task.main, argv[1:]
    if first == "i2v":
        return run_seedance_image_to_video.main, argv[1:]
    if first == "duomi":
        return run_duomi_nano_banana_text2img.main, argv[1:]

    if first == "video":
        if len(argv) == 1:
            return None, []
        second = argv[1]
        if second == "run":
            return run_seedance_task.main, argv[2:]
        if second == "i2v":
            return run_seedance_image_to_video.main, argv[2:]
        return None, []

    if first == "image":
        if len(argv) == 1:
            return None, []
        second = argv[1]
        if second == "t2i":
            return run_duomi_nano_banana_text2img.main, argv[2:]
        return None, []

    return None, []


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)

    if not argv or argv[0] in {"-h", "--help"}:
        parser = build_parser()
        parser.print_help()
        print("")
        print("Quick examples:")
        print("  seedance video run --prompt \"...\" --duration 5")
        print("  seedance video i2v --prompt \"...\" --image-url \"https://...\"")
        print("  seedance image t2i --prompt \"...\"")
        print("")
        print("Tip: You can still pass old flags directly:")
        print("  seedance --prompt \"...\" --ratio 16:9")
        return 0

    runner, forwarded = dispatch(argv)
    if runner is None:
        parser = build_parser()
        parser.print_usage(sys.stderr)
        print("Invalid command. Use --help for supported subcommands.", file=sys.stderr)
        return 2

    return runner(forwarded)


if __name__ == "__main__":
    sys.exit(main())

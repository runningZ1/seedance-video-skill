#!/usr/bin/env python3
"""Unified CLI entrypoint for Seedance video workflows."""

from __future__ import annotations

import argparse
import sys
from typing import Callable

import run_seedance_image_to_video
import run_seedance_task


Runner = Callable[[list[str] | None], int]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="seedance",
        description="Unified CLI for Seedance video generation.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="seedance-cli 1.0",
    )

    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("video", help="General Seedance video workflow")
    subparsers.add_parser("image-to-video", help="Seedance image-to-video workflow")

    return parser


def dispatch(argv: list[str]) -> tuple[Runner | None, list[str]]:
    if not argv:
        return run_seedance_task.main, []

    first = argv[0]
    if first.startswith("-"):
        return run_seedance_task.main, argv

    if first == "video":
        return run_seedance_task.main, argv[1:]
    if first == "image-to-video":
        return run_seedance_image_to_video.main, argv[1:]

    return None, []


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)

    if not argv or argv[0] in {"-h", "--help"}:
        parser = build_parser()
        parser.print_help()
        print("")
        print("Quick examples:")
        print("  seedance video --prompt \"...\" --duration 5")
        print("  seedance image-to-video --prompt \"...\" --image-url \"https://...\"")
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

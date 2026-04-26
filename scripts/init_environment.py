#!/usr/bin/env python3
"""
Seedance Video Generation - Development Environment Initialization

This script sets up the Python environment for Seedance video generation.
It will:
1. Check for Python 3.10+ installation
2. Create a virtual environment (.venv)
3. Install required dependencies (volcengine-python-sdk[ark])
4. Create convenient run scripts

Usage:
    python init_environment.py          # Interactive mode
    python init_environment.py --quiet   # Non-interactive mode (use existing tools if available)
    python init_environment.py --help    # Show help
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


VENV_NAME = ".venv"
REQUIRED_PYTHON_VERSION = (3, 10)
REQUIRED_PACKAGES = ["volcengine-python-sdk[ark]"]
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent


def get_python_command() -> str | None:
    """Find the best Python command available."""
    for cmd in ["python3", "python", "py"]:
        try:
            result = subprocess.run(
                [cmd, "--version"],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                return cmd
        except (FileNotFoundError, OSError):
            continue
    return None


def check_python_version(python_cmd: str) -> tuple[bool, str]:
    """Check if Python version meets requirements."""
    try:
        result = subprocess.run(
            [python_cmd, "--version"],
            capture_output=True,
            text=True,
        )
        version_str = result.stdout.strip() or result.stderr.strip()
        version_str = version_str.replace("Python ", "").split(".")[:2]
        version = tuple(int(x) for x in version_str)
        meets_req = version >= REQUIRED_PYTHON_VERSION
        return meets_req, f"{version[0]}.{version[1]}"
    except Exception as e:
        return False, f"Unknown ({e})"


def find_or_create_venv(python_cmd: str, venv_path: Path, quiet: bool = False) -> bool:
    """Create virtual environment if it doesn't exist."""
    if venv_path.exists():
        if not quiet:
            print(f"  Virtual environment already exists: {venv_path}")
        return True

    if not quiet:
        print(f"  Creating virtual environment at {venv_path}...")

    try:
        subprocess.run(
            [python_cmd, "-m", "venv", str(venv_path)],
            check=True,
            capture_output=True,
        )
        if not quiet:
            print(f"  Virtual environment created successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  Error creating virtual environment: {e}", file=sys.stderr)
        return False


def get_venv_python(venv_path: Path) -> Path:
    """Get the Python executable path within the venv."""
    if sys.platform == "win32":
        return venv_path / "Scripts" / "python.exe"
    return venv_path / "bin" / "python"


def get_venv_pip(venv_path: Path) -> Path:
    """Get the pip executable path within the venv."""
    if sys.platform == "win32":
        return venv_path / "Scripts" / "pip.exe"
    return venv_path / "bin" / "pip"


def install_packages(venv_pip: Path, packages: list[str], quiet: bool = False) -> bool:
    """Install required packages into the virtual environment."""
    if not quiet:
        print(f"  Installing packages: {', '.join(packages)}...")

    try:
        subprocess.run(
            [str(venv_pip), "install"] + packages,
            check=True,
            capture_output=True,
        )
        if not quiet:
            print(f"  Packages installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  Error installing packages: {e}", file=sys.stderr)
        return False


def check_uv_available() -> bool:
    """Check if uv is available."""
    try:
        subprocess.run(
            ["uv", "--version"],
            capture_output=True,
            check=True,
        )
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def install_with_uv(venv_path: Path, packages: list[str], quiet: bool = False) -> bool:
    """Install packages using uv (faster)."""
    if not quiet:
        print(f"  Installing with uv (faster)...")

    try:
        subprocess.run(
            ["uv", "pip", "install"] + packages + ["--python", str(venv_path)],
            check=True,
            capture_output=True,
        )
        if not quiet:
            print(f"  Packages installed successfully.")
        return True
    except subprocess.CalledProcessError:
        return False


def create_run_scripts(venv_path: Path, skill_root: Path, quiet: bool = False) -> None:
    """Create convenient run scripts."""
    scripts_dir = skill_root

    if sys.platform == "win32":
        # Windows batch file
        script_content = f'''@echo off
REM Seedance Video Generation - Environment Activation
REM This script activates the virtual environment and shows usage examples.

cd /d "{skill_root}"
call "{venv_path}\\Scripts\\activate.bat"

echo.
echo ==========================================================
echo   Seedance Video Generation Environment Activated
echo ==========================================================
echo.
echo Usage examples:
echo   1. Text to video:
echo      python scripts\\seedance_cli.py video run --prompt "你的创意描述"
echo.
echo   2. Image to video:
echo      python scripts\\seedance_cli.py video i2v --prompt "你的描述" --image-url "https://example.com/image.png"
echo.
echo   3. Video editing:
echo      python scripts\\seedance_cli.py video run --prompt "替换视频中的物品" --video-url "https://example.com/video.mp4" --image-url "https://example.com/image.png"
echo.
echo   Full options: python scripts\\seedance_cli.py --help
echo.

if "%1"=="" goto :end
python scripts\\seedance_cli.py %*
:end
pause
'''
        script_path = scripts_dir / "seedance.bat"
        script_path.write_text(script_content, encoding="utf-8")
        if not quiet:
            print(f"  Created: {script_path}")

    else:
        # Unix shell script
        script_content = f'''#!/bin/bash
# Seedance Video Generation - Environment Activation
# This script activates the virtual environment and shows usage examples.

cd "{skill_root}"
source "{venv_path}/bin/activate"

echo ""
echo "=================================================="
echo "   Seedance Video Generation Environment Activated"
echo "=================================================="
echo ""
echo "Usage examples:"
echo "  1. Text to video:"
echo "     python scripts/seedance_cli.py video run --prompt '你的创意描述'"
echo ""
echo "  2. Image to video:"
echo "     python scripts/seedance_cli.py video i2v --prompt '你的描述' --image-url 'https://example.com/image.png'"
echo ""
echo "  3. Video editing:"
echo "     python scripts/seedance_cli.py video run --prompt '替换视频中的物品' --video-url 'https://example.com/video.mp4' --image-url 'https://example.com/image.png'"
echo ""
echo "  Full options: python scripts/seedance_cli.py --help"
echo ""

if [ $# -eq 0 ]; then
    echo "No arguments provided. Showing help:"
    python scripts/seedance_cli.py --help
else
    python scripts/seedance_cli.py "$@"
fi
'''
        script_path = scripts_dir / "seedance.sh"
        script_path.write_text(script_content, encoding="utf-8")
        script_path.chmod(0o755)
        if not quiet:
            print(f"  Created: {script_path}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Initialize the Seedance video generation development environment.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python init_environment.py              # Interactive setup
  python init_environment.py --quiet     # Non-interactive (use existing tools)
  python init_environment.py --skip-venv # Only check Python, don't create venv
        """,
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Non-interactive mode: use existing tools if available",
    )
    parser.add_argument(
        "--skip-venv",
        action="store_true",
        help="Skip virtual environment creation",
    )
    parser.add_argument(
        "--python",
        default=None,
        help="Python command to use (default: auto-detect)",
    )

    args = parser.parse_args()

    print("=" * 60)
    print("  Seedance Video Generation - Environment Setup")
    print("=" * 60)
    print()

    # Step 1: Check Python
    print("[1/4] Checking Python installation...")
    python_cmd = args.python or get_python_command()
    if not python_cmd:
        print("  ERROR: Python not found. Please install Python 3.10 or later.")
        print("  Download: https://www.python.org/downloads/")
        return 1

    meets_req, version = check_python_version(python_cmd)
    if not meets_req:
        print(f"  ERROR: Python {version} found, but Python {REQUIRED_PYTHON_VERSION[0]}.{REQUIRED_PYTHON_VERSION[1]}+ is required.")
        return 1
    print(f"  Found: Python {version}")

    if args.skip_venv:
        print()
        print("Skipping virtual environment creation (--skip-venv).")
        return 0

    # Step 2: Create virtual environment
    print()
    print("[2/4] Setting up virtual environment...")
    venv_path = SKILL_ROOT / VENV_NAME

    if venv_path.exists() and not args.quiet:
        print(f"  Virtual environment already exists at {venv_path}")

        # Check if it's functional
        venv_python = get_venv_python(venv_path)
        if venv_python.exists():
            print("  Using existing virtual environment.")
        else:
            print("  Virtual environment appears broken. Recreating...")
            import shutil
            shutil.rmtree(venv_path)
            find_or_create_venv(python_cmd, venv_path, args.quiet)
    else:
        find_or_create_venv(python_cmd, venv_path, args.quiet)

    if not venv_path.exists():
        print("  ERROR: Failed to create virtual environment.")
        return 1

    venv_python = get_venv_python(venv_path)
    venv_pip = get_venv_pip(venv_path)

    # Step 3: Install dependencies
    print()
    print("[3/4] Installing dependencies...")

    # Try uv first if available (faster)
    if check_uv_available():
        success = install_with_uv(venv_path, REQUIRED_PACKAGES, args.quiet)
    else:
        success = install_packages(venv_pip, REQUIRED_PACKAGES, args.quiet)

    if not success:
        print("  ERROR: Failed to install dependencies.")
        print("  You can try installing manually:")
        print(f"    {venv_pip} install {' '.join(REQUIRED_PACKAGES)}")
        return 1

    # Step 4: Create run scripts
    print()
    print("[4/4] Creating run scripts...")
    create_run_scripts(venv_path, SKILL_ROOT, args.quiet)

    print()
    print("=" * 60)
    print("  Setup Complete!")
    print("=" * 60)
    print()
    print("You can now use Seedance Video Generation:")
    print()

    if sys.platform == "win32":
        print("  Quick start: Double-click seedance.bat or run:")
        print("    seedance.bat")
        print()
        print("  Or manually activate:")
        print(f"    call {venv_path}\\Scripts\\activate.bat")
    else:
        print("  Quick start: Run:")
        print("    ./seedance.sh")
        print()
        print("  Or manually activate:")
        print(f"    source {venv_path}/bin/activate")

    print()
    print("Example commands:")
    print("  python scripts/seedance_cli.py video run --prompt '日出时分的海边风景' --ratio 16:9 --duration 5")
    print("  python scripts/seedance_cli.py --help")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())

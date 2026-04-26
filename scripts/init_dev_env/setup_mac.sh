#!/bin/bash

# Seedance Video Generation - Development Environment Setup (macOS/Linux)
# Uses uv to manage Python and dependencies automatically.
# This script is self-contained and can be run from anywhere.

set -e

# Ensure we are working in the script directory context
cd "$(dirname "$0")"

# Go to parent directory (scripts/ -> skill root)
cd "../../"

SKILL_ROOT="$(pwd)"

echo "=================================================="
echo "   Initializing Seedance Development Environment..."
echo "=================================================="
echo ""

# 1. Setup uv (Download if not present)
UV_CMD="uv"

if command -v uv &> /dev/null; then
    echo "[1/4] uv tool found in system PATH."
elif [ -f "./uv" ]; then
    echo "[1/4] uv tool found in current directory."
    UV_CMD="./uv"
else
    echo "[1/4] Downloading uv tool..."
    echo ""
    echo "Official installation guide: https://docs.astral.sh/uv/getting-started/installation/"
    echo ""

    # Install using official script
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Try to find where it was installed
    if [ -f "$HOME/.local/bin/uv" ]; then
        UV_CMD="$HOME/.local/bin/uv"
    elif [ -f "$HOME/.cargo/bin/uv" ]; then
        UV_CMD="$HOME/.cargo/bin/uv"
    else
        export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
        if command -v uv &> /dev/null; then
            UV_CMD="uv"
        else
            echo "Error: uv installed but not found in common locations. Please restart your terminal."
            exit 1
        fi
    fi
fi

# 2. Create Virtual Environment
echo "[2/4] Creating virtual environment (.venv)..."
"$UV_CMD" venv .venv --python 3.12

# 3. Install Dependencies
echo "[3/4] Installing SDK (volcengine-python-sdk[ark])..."
"$UV_CMD" pip install "volcengine-python-sdk[ark]" --python .venv

# 4. Create run script
echo "[4/4] Generating run scripts..."

cat <<'EOF' > seedance.sh
#!/bin/bash
cd "$(dirname "$0")"
source .venv/bin/activate

echo "Seedance Video Generation - Quick Start"
echo ""
echo "Usage examples:"
echo "  1. Text to video:"
echo "     python scripts/run_seedance_task.py --prompt '你的创意描述'"
echo ""
echo "  2. Image to video:"
echo "     python scripts/run_seedance_task.py --prompt '你的描述' --image-url 'https://example.com/image.png'"
echo ""
echo "  3. Video editing:"
echo "     python scripts/run_seedance_task.py --prompt '替换视频中的物品' --video-url 'https://example.com/video.mp4' --image-url 'https://example.com/image.png'"
echo ""
echo "  For more options: python scripts/run_seedance_task.py --help"

if [ $# -eq 0 ]; then
    echo ""
    echo "No arguments provided. Showing help:"
    python scripts/run_seedance_task.py --help
fi

if [ $# -gt 0 ]; then
    python scripts/run_seedance_task.py "$@"
fi
EOF

chmod +x seedance.sh

echo ""
echo "=================================================="
echo "   Setup Complete!"
echo "=================================================="
echo ""
echo "You can now use the following commands:"
echo ""
echo "  ./seedance.sh                  - Show usage examples"
echo "  ./seedance.sh --help           - Show all options"
echo ""
echo "Or activate the environment manually:"
echo "  source .venv/bin/activate"
echo ""
echo "Example commands:"
echo "  python scripts/run_seedance_task.py --prompt '日出时分的海边风景' --ratio 16:9 --duration 5"
echo "  python scripts/run_seedance_task.py --help"
echo ""

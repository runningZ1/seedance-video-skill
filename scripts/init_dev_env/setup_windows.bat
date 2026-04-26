@echo off
setlocal EnableDelayedExpansion

REM Seedance Video Generation - Development Environment Setup (Windows)
REM Uses uv to manage Python and dependencies automatically.
REM
REM This script is self-contained and can be run from anywhere.

REM Ensure we are working in the script directory context
cd /d "%~dp0"

REM Go to parent directory (scripts/ -> skill root)
cd /d "%~dp0..\.."

echo ==========================================================
echo   Initializing Seedance Development Environment...
echo ==========================================================
echo.

REM 1. Setup uv (Download if not present)
set "UV_CMD=uv"

where uv >nul 2>&1
if !errorlevel! EQU 0 (
    echo [1/4] uv tool found in system PATH.
    goto :SKIP_DOWNLOAD
)

if exist "uv.exe" (
    echo [1/4] uv tool found in current directory.
    set "UV_CMD=.\uv.exe"
    goto :SKIP_DOWNLOAD
)

echo [1/4] Downloading uv tool...
echo.
echo Official installation guide: https://docs.astral.sh/uv/getting-started/installation/
echo.

powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

where uv >nul 2>&1
if !errorlevel! EQU 0 (
    echo uv installed successfully to PATH.
    set "UV_CMD=uv"
    goto :SKIP_DOWNLOAD
)

if exist "%USERPROFILE%\.cargo\bin\uv.exe" (
    set "UV_CMD=%USERPROFILE%\.cargo\bin\uv.exe"
    echo uv installed to %USERPROFILE%\.cargo\bin\uv.exe
    goto :SKIP_DOWNLOAD
)

REM Fallback: Download standalone binary
echo Standard installation did not make 'uv' available immediately. Trying standalone download...
powershell -Command "try { Invoke-WebRequest -Uri 'https://github.com/astral-sh/uv/releases/latest/download/uv-x86_64-pc-windows-msvc.zip' -OutFile 'uv.zip' -ErrorAction Stop } catch { exit 1 }"

if !errorlevel! NEQ 0 (
    echo [Error] Failed to download uv.
    echo Please check your network connection.
    echo You can manually download uv from: https://github.com/astral-sh/uv/releases/latest/download/uv-x86_64-pc-windows-msvc.zip
    echo And extract 'uv.exe' to: "%~dp0..\.."
    pause
    exit /b 1
)

echo Extracting uv...
powershell -Command "Expand-Archive -Path 'uv.zip' -DestinationPath '.' -Force"

if exist "uv-x86_64-pc-windows-msvc\uv.exe" (
    move /y "uv-x86_64-pc-windows-msvc\uv.exe" . >nul
    rmdir /s /q "uv-x86_64-pc-windows-msvc"
    set "UV_CMD=.\uv.exe"
)
if exist "uv.zip" del uv.zip

:SKIP_DOWNLOAD

REM 2. Create Virtual Environment
echo [2/4] Creating virtual environment (.venv)...
%UV_CMD% venv ".venv" --python 3.10

if !errorlevel! NEQ 0 (
    echo Error: Failed to create virtual environment.
    pause
    exit /b 1
)

REM 3. Install Dependencies
echo [3/4] Installing SDK (volcengine-python-sdk[ark])...
%UV_CMD% pip install "volcengine-python-sdk[ark]" --python ".venv"

if !errorlevel! NEQ 0 (
    echo Error: Failed to install dependencies.
    pause
    exit /b 1
)

REM 4. Create run script
echo [4/4] Generating run scripts...

(
echo @echo off
echo cd /d "%%~dp0"
echo call .venv\Scripts\activate.bat
echo python scripts\seedance_cli.py --help
echo pause
) > "run_seedance.bat"

(
echo @echo off
echo REM Seedance Video Generation - Quick Start
echo cd /d "%%~dp0"
echo call .venv\Scripts\activate.bat
echo.
echo echo Starting Seedance Video Generation...
echo echo.
echo echo Usage examples:
echo echo   1. Text to video:
echo echo      python scripts\seedance_cli.py video --prompt "你的创意描述"
echo echo.
echo echo   2. Image to video:
echo echo      python scripts\seedance_cli.py image-to-video --prompt "你的描述" --image-url "https://example.com/image.png"
echo echo.
echo echo   3. Video editing:
echo echo      python scripts\seedance_cli.py video --prompt "替换视频中的物品" --video-url "https://example.com/video.mp4" --image-url "https://example.com/image.png"
echo echo.
echo if "%%1"=="" goto :end
echo python scripts\seedance_cli.py %%*
echo :end
echo pause
) > "seedance.bat"

echo.
echo ==========================================================
echo   Setup Complete!
echo ==========================================================
echo.
echo You can now use the following commands:
echo.
echo   seedance.bat                  - Show usage examples
echo   seedance.bat --help           - Show all options
echo.
echo Or activate the environment manually:
echo   call .venv\Scripts\activate.bat
echo.
echo Example commands:
echo   python scripts\seedance_cli.py video --prompt "日出时分的海边风景" --ratio 16:9 --duration 5
echo   python scripts\seedance_cli.py --help
echo.
pause

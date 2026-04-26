#Requires -Version 5.1
<#
.SYNOPSIS
    Seedance Video Generation - Development Environment Setup (Windows PowerShell)

.DESCRIPTION
    This script sets up the Python environment for Seedance video generation on Windows.
    It will:
    1. Check for Python 3.10+ installation
    2. Create a virtual environment (.venv)
    3. Install required dependencies (volcengine-python-sdk[ark])
    4. Create convenient run scripts

    Supports: Windows 10/11 with PowerShell 5.1+

.PARAMETER Quiet
    Non-interactive mode: use existing tools if available, skip confirmations

.PARAMETER SkipVenv
    Skip virtual environment creation

.EXAMPLE
    .\setup_windows.ps1
    Run with full output and confirmations

.EXAMPLE
    .\setup_windows.ps1 -Quiet
    Non-interactive mode - faster execution

.EXAMPLE
    .\setup_windows.ps1 -SkipVenv
    Only check Python, don't create venv
#>

param(
    [switch]$Quiet,
    [switch]$SkipVenv
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

# Resolve skill root from script path (scripts/init_dev_env -> project root)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$SkillRoot = (Resolve-Path (Join-Path $ScriptDir "..\..")).Path
Set-Location $SkillRoot

$VenvName = ".venv"
$RequiredPythonVersion = [version]"3.10"
$RequiredPackages = @("volcengine-python-sdk[ark]")

function Write-Step {
    param([string]$Message)
    Write-Host "" -ForegroundColor Cyan
    Write-Host "[$((Get-Location).Name)] $Message" -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Message)
    Write-Host "  SUCCESS: $Message" -ForegroundColor Green
}

function Write-Error {
    param([string]$Message)
    Write-Host "  ERROR: $Message" -ForegroundColor Red
}

function Write-Info {
    param([string]$Message)
    Write-Host "  $Message" -ForegroundColor Gray
}

# Check Python installation
Write-Step "Checking Python installation..."

$PythonCmd = $null
foreach ($cmd in @("python", "python3", "py")) {
    try {
        $result = & $cmd --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            $PythonCmd = $cmd
            break
        }
    } catch {
        continue
    }
}

if (-not $PythonCmd) {
    Write-Error "Python not found. Please install Python 3.10 or later."
    Write-Host "Download: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

$PythonVersion = & $PythonCmd --version 2>&1
$PythonVersion = $PythonVersion -replace "Python ", ""
try {
    $VersionObj = [version]$PythonVersion
    if ($VersionObj -lt $RequiredPythonVersion) {
        Write-Error "Python $PythonVersion found, but Python $RequiredPythonVersion+ is required."
        exit 1
    }
} catch {
    Write-Error "Could not parse Python version: $PythonVersion"
    exit 1
}

Write-Success "Found Python $PythonVersion"
$PythonCmd = (Get-Command $PythonCmd).Source

if ($SkipVenv) {
    Write-Step "Skipping virtual environment creation (-SkipVenv)."
    exit 0
}

# Check if uv is available (faster package manager)
$UvAvailable = $false
try {
    $null = Get-Command uv -ErrorAction SilentlyContinue
    if ($LASTEXITCODE -eq 0 -or (Test-Path "uv.exe")) {
        $UvAvailable = $true
        if (-not $Quiet) { Write-Info "uv package manager found (will be used for faster installation)" }
    }
} catch {
    $UvAvailable = $false
}

# Create virtual environment
Write-Step "Setting up virtual environment..."
$VenvPath = Join-Path $SkillRoot $VenvName

if (Test-Path $VenvPath) {
    $VenvPython = if ($IsWindows -or -not $IsWindows) {
        Join-Path $VenvPath "Scripts\python.exe"
    } else {
        Join-Path $VenvPath "bin\python"
    }

    if (Test-Path $VenvPython) {
        if (-not $Quiet) { Write-Info "Virtual environment already exists at $VenvPath" }
    } else {
        Write-Info "Virtual environment appears broken. Recreating..."
        Remove-Item -Recurse -Force $VenvPath
        & $PythonCmd -m venv $VenvPath
    }
} else {
    Write-Info "Creating virtual environment at $VenvPath..."
    & $PythonCmd -m venv $VenvPath
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to create virtual environment"
        exit 1
    }
}

$VenvPython = Join-Path $VenvPath "Scripts\python.exe"
$VenvPip = Join-Path $VenvPath "Scripts\pip.exe"

if (-not (Test-Path $VenvPython)) {
    Write-Error "Virtual environment Python not found at expected location"
    exit 1
}

Write-Success "Virtual environment ready"

# Install dependencies
Write-Step "Installing dependencies..."

if ($UvAvailable) {
    Write-Info "Installing with uv (faster)..."
    $uvCmd = Get-Command uv -ErrorAction SilentlyContinue
    if ($uvCmd.Source) {
        $uvExe = $uvCmd.Source
    } elseif (Test-Path ".\uv.exe") {
        $uvExe = ".\uv.exe"
    } else {
        $uvExe = "uv"
    }

    try {
        & $uvExe pip install $RequiredPackages --python $VenvPython
        $InstallSuccess = $LASTEXITCODE -eq 0
    } catch {
        $InstallSuccess = $false
    }

    if ($InstallSuccess) {
        Write-Success "Packages installed via uv"
    } else {
        Write-Info "uv installation failed, falling back to pip..."
        & $VenvPip install $RequiredPackages
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Failed to install packages"
            exit 1
        }
        Write-Success "Packages installed via pip"
    }
} else {
    Write-Info "Installing with pip..."
    & $VenvPip install $RequiredPackages
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to install packages"
        exit 1
    }
    Write-Success "Packages installed"
}

# Create run scripts
Write-Step "Creating run scripts..."

# Create seedance.bat
$BatContent = @"
@echo off
REM Seedance Video Generation - Quick Start Script
REM This script activates the virtual environment

cd /d "$SkillRoot"
call "$VenvPath\Scripts\activate.bat"

echo.
echo ==========================================================
echo   Seedance Video Generation Environment
echo ==========================================================
echo.
echo Usage examples:
echo   1. Text to video:
echo      python scripts\seedance_cli.py video --prompt "你的创意描述"
echo.
echo   2. Image to video:
echo      python scripts\seedance_cli.py image-to-video --prompt "你的描述" --image-url "https://example.com/image.png"
echo.
echo   3. Video editing:
echo      python scripts\seedance_cli.py video --prompt "替换视频中的物品" --video-url "https://example.com/video.mp4" --image-url "https://example.com/image.png"
echo.
echo   Full options: python scripts\seedance_cli.py --help
echo.

if "%1"=="" goto :end
python scripts\seedance_cli.py %*
:end
pause
"@

$BatPath = Join-Path $SkillRoot "seedance.bat"
$BatContent | Out-File -FilePath $BatPath -Encoding UTF8
Write-Info "Created: seedance.bat"

# Create seedance.ps1 (PowerShell version)
$Ps1Content = @'
# Seedance Video Generation - Quick Start Script (PowerShell)
# This script activates the virtual environment

$SkillRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $SkillRoot
$VenvPath = Join-Path $SkillRoot ".venv"

if (-not (Test-Path (Join-Path $VenvPath "Scripts\Activate.ps1"))) {
    Write-Error "Virtual environment not found. Run setup_windows.ps1 first."
    exit 1
}

& (Join-Path $VenvPath "Scripts\Activate.ps1")

Write-Host ""
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  Seedance Video Generation Environment" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Usage examples:"
Write-Host "  1. Text to video:"
Write-Host "     python scripts\seedance_cli.py video --prompt `"你的创意描述`""
Write-Host ""
Write-Host "  2. Image to video:"
Write-Host "     python scripts\seedance_cli.py image-to-video --prompt `"你的描述`" --image-url `"https://example.com/image.png`""
Write-Host ""
Write-Host "  3. Video editing:"
Write-Host "     python scripts\seedance_cli.py video --prompt `"替换视频中的物品`" --video-url `"https://example.com/video.mp4`" --image-url `"https://example.com/image.png`""
Write-Host ""
Write-Host "  Full options: python scripts\seedance_cli.py --help"
Write-Host ""

if ($Args.Count -eq 0) {
    Write-Host "No arguments provided. Showing help:"
    & python scripts\seedance_cli.py --help
} else {
    & python scripts\seedance_cli.py $Args
}
'@

$Ps1Path = Join-Path $SkillRoot "seedance.ps1"
$Ps1Content | Out-File -FilePath $Ps1Path -Encoding UTF8
Write-Info "Created: seedance.ps1"

# Create .env.example if it doesn't exist
$EnvExamplePath = Join-Path $SkillRoot ".env.example"
if (-not (Test-Path $EnvExamplePath)) {
    @"
# Seedance Video Generation - Environment Configuration
# Copy this file to .env and fill in your values

# Ark API Key (required)
ARK_API_KEY=your_api_key_here

# Default model (optional)
# doubao-seedance-2-0-260128 - Quality mode
# doubao-seedance-2-0-fast-260128 - Speed mode
SEEDANCE_MODEL_DEFAULT=doubao-seedance-2-0-260128
"@ | Out-File -FilePath $EnvExamplePath -Encoding UTF8
    Write-Info "Created: .env.example"
}

Write-Host ""
Write-Host "==========================================================" -ForegroundColor Green
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
Write-Host ""
Write-Host "You can now use Seedance Video Generation:" -ForegroundColor White
Write-Host ""
Write-Host "  Quick start (PowerShell):" -ForegroundColor Yellow
Write-Host "    .\seedance.ps1" -ForegroundColor Gray
Write-Host ""
Write-Host "  Quick start (CMD/Bat):" -ForegroundColor Yellow
Write-Host "    seedance.bat" -ForegroundColor Gray
Write-Host ""
Write-Host "  Manual activation:" -ForegroundColor Yellow
Write-Host "    & .\.venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host ""
Write-Host "Example commands:" -ForegroundColor White
Write-Host '  python scripts\seedance_cli.py video --prompt "日出时分的海边风景" --ratio 16:9 --duration 5' -ForegroundColor Gray
Write-Host "  python scripts\seedance_cli.py --help" -ForegroundColor Gray
Write-Host ""

if (-not $Quiet) {
    Write-Host "Press any key to exit..." -ForegroundColor DarkGray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

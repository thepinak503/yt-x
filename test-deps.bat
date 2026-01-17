@echo off
REM Test script for yt-x
REM This script verifies all dependencies and tests basic functionality

echo ========================================
echo yt-x Dependency Check and Test
echo ========================================
echo.

set ERROR_FOUND=0

REM Check Python
echo [1/5] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [FAIL] Python not found
    set ERROR_FOUND=1
) else (
    echo [OK] Python found
    python --version
)
echo.

REM Check yt-dlp
echo [2/5] Checking yt-dlp...
yt-dlp --version >nul 2>&1
if errorlevel 1 (
    echo [WARN] yt-dlp not found (required for YouTube data)
    echo Install: winget install yt-dlp
    set ERROR_FOUND=1
) else (
    echo [OK] yt-dlp found
    yt-dlp --version 2>&1 | find "version"
)
echo.

REM Check VLC
echo [3/5] Checking VLC...
vlc --version >nul 2>&1
if errorlevel 1 (
    echo [WARN] VLC not found (optional but recommended)
    echo Install: winget install VideoLAN.VLC
) else (
    echo [OK] VLC found
    vlc --version 2>&1 | find "version"
)
echo.

REM Check mpv
echo [4/5] Checking mpv...
mpv --version >nul 2>&1
if errorlevel 1 (
    echo [WARN] mpv not found (optional)
    echo Install: winget install mpv-player.mpv
) else (
    echo [OK] mpv found
    mpv --version 2>&1 | find "mpv"
)
echo.

REM Check Python dependencies
echo [5/5] Checking Python dependencies...
python -c "import textual" >nul 2>&1
if errorlevel 1 (
    echo [FAIL] textual not installed
    set ERROR_FOUND=1
) else (
    echo [OK] textual installed
)

python -c "import rich" >nul 2>&1
if errorlevel 1 (
    echo [FAIL] rich not installed
    set ERROR_FOUND=1
) else (
    echo [OK] rich installed
)

python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo [FAIL] requests not installed
    set ERROR_FOUND=1
) else (
    echo [OK] requests installed
)

python -c "import platformdirs" >nul 2>&1
if errorlevel 1 (
    echo [FAIL] platformdirs not installed
    set ERROR_FOUND=1
) else (
    echo [OK] platformdirs installed
)
echo.

echo ========================================
echo Summary
echo ========================================

if "%ERROR_FOUND%"=="1" (
    echo Status: [FAIL] Some dependencies are missing
    echo.
    echo Please install missing dependencies:
    echo   pip install -r requirements.txt
    echo   winget install yt-dlp
    echo   winget install VideoLAN.VLC
) else (
    echo Status: [OK] All dependencies are installed
    echo.
    echo You can run yt-x:
    echo   python yt-x.py
    echo   Or: .\yt-x.bat
    echo   Or: .\yt-x.exe (if built)
)

echo.
pause

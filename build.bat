@echo off
REM Build script for yt-x Windows executable using Nuitka

echo ========================================
echo Building yt-x Windows Executable
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo Python version:
python --version
echo.

REM Install build dependencies
echo [1/4] Installing build dependencies...
pip install Nuitka ordered-set zstandard zimport
if errorlevel 1 (
    echo Error: Failed to install build dependencies
    pause
    exit /b 1
)
echo Build dependencies installed successfully.
echo.

REM Install runtime dependencies
echo [2/4] Installing runtime dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install runtime dependencies
    pause
    exit /b 1
)
echo Runtime dependencies installed successfully.
echo.

REM Create dist directory
if not exist dist mkdir dist

REM Build with Nuitka
echo [3/4] Building executable with Nuitka...
echo This may take a few minutes...

python -m nuitka ^
    --standalone ^
    --onefile ^
    --windows-disable-console ^
    --assume-yes-for-downloads ^
    --output-dir=dist ^
    --output-filename=yt-x.exe ^
    --enable-plugin=anti-bloat ^
    --follow-imports ^
    --include-package-data=textual ^
    --include-package-data=rich ^
    --include-package-data=ytdlp ^
    --include-module=requests ^
    --include-module=platformdirs ^
    yt-x.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo Build FAILED
    echo ========================================
    echo.
    echo Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo [4/4] Build completed successfully!
echo ========================================
echo.
echo Executable location: dist\yt-x.exe
echo.
echo File size:
dir dist\yt-x.exe | find "yt-x.exe"
echo.
echo ========================================
echo READY TO USE!
echo ========================================
echo.
echo You can now run yt-x by executing:
echo   dist\yt-x.exe
echo.
echo To install, copy dist\yt-x.exe to a folder in your PATH.
echo.
pause

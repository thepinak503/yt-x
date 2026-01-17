@echo off
REM Build script for yt-x Windows executable

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

REM Install build dependencies
echo Installing build dependencies...
pip install Nuitka ordered-set zstandard
if errorlevel 1 (
    echo Error: Failed to install build dependencies
    pause
    exit /b 1
)
echo.

REM Install runtime dependencies
echo Installing runtime dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install runtime dependencies
    pause
    exit /b 1
)
echo.

REM Build with Nuitka
echo Building executable with Nuitka...
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
    yt-x.py

if errorlevel 1 (
    echo.
    echo Error: Build failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build completed successfully!
echo ========================================
echo.
echo Executable location: dist\yt-x.exe
echo.
echo You can now run yt-x by executing:
echo   dist\yt-x.exe
echo.
pause

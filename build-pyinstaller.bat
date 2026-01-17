@echo off
REM Build script for yt-x Windows executable using PyInstaller

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

REM Install runtime dependencies
echo [1/3] Installing runtime dependencies...
pip install -r requirements.txt -q
if errorlevel 1 (
    echo Error: Failed to install runtime dependencies
    pause
    exit /b 1
)
echo Runtime dependencies installed successfully.
echo.

REM Create dist directory
if not exist dist mkdir dist

REM Build with PyInstaller
echo [2/3] Building executable with PyInstaller...
echo This may take a few minutes...

pyinstaller --onefile ^
    --windowed ^
    --name yt-x ^
    --icon=NONE ^
    --add-data "yt_x;yt_x" ^
    --hidden-import textual ^
    --hidden-import rich ^
    --hidden-import requests ^
    --hidden-import platformdirs ^
    --clean ^
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
echo [3/3] Build completed successfully!
echo ========================================
echo.
echo Executable location: dist\yt-x.exe
echo.

REM Get file size
for %%I in (dist\yt-x.exe) do set SIZE=%%~zI
echo File size: %SIZE% bytes
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

REM Test if exe was created
if exist dist\yt-x.exe (
    echo Executable created successfully!
) else (
    echo WARNING: Executable was not created!
    echo Check the error messages above.
)
echo.
pause

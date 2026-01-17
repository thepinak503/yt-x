# Build Instructions for yt-x

This document explains how to build yt-x on Windows.

## Prerequisites

- Python 3.8-3.14 (3.10+ recommended for best compatibility)
  - Note: Python 3.15+ may have build tool compatibility issues
  - Download from https://www.python.org/downloads/
- pip (Python package manager)
- git (for cloning repository)

## Quick Start

### Option 1: Use Pre-built EXE (Recommended)

Download from: https://github.com/thepinak503/yt-x/releases

1. Download `yt-x.exe`
2. Place in desired location
3. Run by double-clicking or from command line

### Option 2: Use Batch File Launcher

The `yt-x.bat` file is a portable launcher:

1. Ensure Python 3.8+ is in PATH
2. Double-click `yt-x.bat`
3. It will automatically install dependencies if needed

### Option 3: Build EXE Yourself

#### Step 1: Clone Repository

```powershell
git clone https://github.com/thepinak503/yt-x.git
cd yt-x
```

#### Step 2: Install Python Dependencies

```powershell
pip install -r requirements.txt
```

#### Step 3: Build Using PyInstaller (Recommended)

```powershell
# Install PyInstaller
pip install pyinstaller

# Build EXE
pyinstaller --onefile --windowed --name yt-x --add-data "yt_x;yt_x" --clean yt-x.py

# The EXE will be created in dist\yt-x.exe
```

Or use the provided build script:

```powershell
.\build-pyinstaller.bat
```

#### Step 4: Build Using Nuitka

```powershell
# Install Nuitka
pip install Nuitka ordered-set zstandard

# Build EXE
python -m nuitka --standalone --onefile --windows-disable-console --output-dir=dist yt-x.py

# The EXE will be created in dist folder
```

Or use the provided build script:

```powershell
.\build.bat
```

## Build Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'imp'"

**Cause**: PyInstaller/Nuitka not compatible with Python 3.15+

**Solution**:
- Use Python 3.8-3.14 instead
- Or use pre-built EXE from releases
- Or use batch file launcher (yt-x.bat)

### Issue: "cffi build failed"

**Cause**: C compiler not found or incompatible Python version

**Solution**:
- Install Microsoft Visual Studio C++ Build Tools
- Or use Python 3.10-3.14
- Or use PyInstaller (requires C compiler but easier setup)

### Issue: "textual module not found"

**Solution**: Install dependencies
```powershell
pip install -r requirements.txt
```

## Testing the Build

After building, test the EXE:

```powershell
# Run the built EXE
.\dist\yt-x.exe

# Or use the batch launcher
.\yt-x.bat
```

Verify:
1. Application starts without errors
2. Main menu appears
3. You can navigate with keyboard
4. Search works
5. Video playback opens VLC/mpv correctly

## Distribution

Once you have a working EXE:

1. Create a release on GitHub
2. Upload `dist/yt-x.exe`
3. Update release notes

### Example Release Notes

```
## yt-x v1.0.0

### Features
- Modern TUI using Textual
- YouTube browsing (feed, trending, subscriptions)
- Video search with filters
- Save videos and track history
- Audio-only mode
- Download support
- VLC m3u8 playlist support
- Windows-native paths and file handling

### Installation
- Download yt-x.exe
- Run yt-x.exe
- No Python installation required (for EXE version)

### Requirements
- Windows 10/11
- yt-dlp (for fetching YouTube data)
- VLC or mpv (for video playback)
```

## Additional Resources

- [PyInstaller Documentation](https://pyinstaller.org/en/stable/)
- [Nuitka Documentation](https://nuitka.net/doc/user-manual.html)
- [Python Downloads](https://www.python.org/downloads/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [VLC](https://www.videolan.org/vlc/)

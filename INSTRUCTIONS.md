# INSTRUCTIONS.md - Complete Setup Guide

**For LLM/AI Agents**: This document contains all necessary instructions to proceed with yt-x development, building, and deployment.

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Installation](#installation)
3. [Building EXE](#building-exe)
4. [Testing](#testing)
5. [Deployment](#deployment)
6. [Troubleshooting](#troubleshooting)
7. [Memory Snapshot](#memory-snapshot)

---

## Quick Start

### For Users (Run Application)

```powershell
# Option 1: Run installer (recommended)
.\install.bat

# Option 2: Run portable
.\yt-x.bat

# Option 3: Use Python
python yt-x.py

# Option 4: Use EXE (when built)
.\dist\yt-x.exe
```

### For Developers (Clone & Modify)

```powershell
# Clone repository
git clone https://github.com/thepinak503/yt-x.git
cd yt-x

# Install dependencies
pip install -r requirements.txt

# Run
python yt-x.py

# Make changes and test
```

---

## Installation

### Method 1: Automatic Installer (Recommended)

This installs yt-x AND all required dependencies.

```powershell
# Run as administrator
.\install.bat
```

**What it does**:
1. Checks for administrator privileges
2. Installs Python 3.10/3.11 via winget
3. Installs yt-dlp via winget
4. Installs VLC via winget
5. Installs mpv via winget
6. Installs Python packages (textual, rich, requests, platformdirs)
7. Copies files to: `C:\Program Files\yt-x` (system) or `%LOCALAPPDATA%\Programs\yt-x` (user)
8. Adds installation directory to PATH
9. Creates desktop shortcut
10. Creates Start Menu shortcut

**Installation Locations**:
- System-wide: `C:\Program Files\yt-x`
- User-specific: `%LOCALAPPDATA%\Programs\yt-x`

**Paths Added to PATH**:
- `C:\Program Files\yt-x`
- OR `%LOCALAPPDATA%\Programs\yt-x`

**Shortcuts Created**:
- Desktop: `yt-x.lnk`
- Start Menu: Programs\yt-x.lnk

### Method 2: Manual Installation

#### Step 1: Install Dependencies

```powershell
# Python 3.8-3.14 (stable version)
winget install Python.Python.3.10 --accept-source-agreements

# yt-dlp (required)
winget install yt-dlp --accept-source-agreements

# VLC (recommended for m3u8 support)
winget install VideoLAN.VLC --accept-source-agreements

# mpv (optional alternative)
winget install mpv-player.mpv --accept-source-agreements
```

#### Step 2: Install Python Packages

```powershell
pip install -r requirements.txt
```

#### Step 3: Run Application

```powershell
# From source
python yt-x.py

# Using batch launcher
.\yt-x.bat
```

### Method 3: Using pip (When Published)

```powershell
# Install from PyPI
pip install yt-x

# Run
yt-x
```

### Method 4: Pre-built EXE (When Available)

```powershell
# Download from releases
# https://github.com/thepinak503/yt-x/releases

# Download yt-x.exe
# Double-click to run

# Or copy to PATH location
copy yt-x.exe C:\Windows\System32\
```

---

## Building EXE

### Requirements

- Python 3.8-3.14 (3.10+ recommended)
- Pip
- Command line with administrator privileges (for system-wide installation)

### Method 1: PyInstaller (Recommended)

**Why PyInstaller**: Better compatibility, easier setup, works with Python 3.8-3.14

#### Step 1: Install PyInstaller

```powershell
pip install pyinstaller
```

#### Step 2: Build EXE

```powershell
# Build single-file executable
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

# Or use provided script
.\build-pyinstaller.bat
```

#### Step 3: Test EXE

```powershell
# Run the built EXE
.\dist\yt-x.exe
```

**Output**: `dist\yt-x.exe`

### Method 2: Nuitka (Advanced)

**Why Nuitka**: Better performance, smaller size, but more complex setup

#### Step 1: Install Nuitka

```powershell
pip install Nuitka ordered-set zstandard zimport
```

#### Step 2: Build EXE

```powershell
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

# Or use provided script
.\build.bat
```

**Output**: `dist\yt-x.exe`

### Method 3: Using Build Scripts

```powershell
# PyInstaller build
.\build-pyinstaller.bat

# Nuitka build
.\build.bat
```

### Build Issues

#### Issue: Python 3.15+ Build Fail

**Symptoms**:
- `ModuleNotFoundError: No module named 'imp'` (PyInstaller)
- `cffi build failed` (Nuitka)
- Other compilation errors

**Causes**:
- PyInstaller/Nuitka don't fully support Python 3.15+
- Build tools not updated for latest Python

**Solutions**:
1. **Use Python 3.8-3.14** (recommended)
   ```powershell
   winget install Python.Python.3.10
   ```
2. **Use pre-built EXE** from releases
3. **Use batch file launcher** (`yt-x.bat`)

#### Issue: Missing C Compiler

**Symptoms**:
- `cffi build failed`
- `error: command 'cl.exe' failed`

**Solution**:
```powershell
# Install Microsoft Visual Studio Build Tools
winget install Microsoft.VisualStudio.2022.BuildTools

# Or install Visual Studio Community
winget install Microsoft.VisualStudio.2022.Community
```

#### Issue: PyInstaller not found

**Solution**:
```powershell
pip install pyinstaller
```

---

## Testing

### Test Dependencies

```powershell
# Run dependency checker
.\test-deps.bat
```

**Expected Output**:
```
[1/5] Checking Python...
[OK] Python found
Python 3.10.11 ...

[2/5] Checking yt-dlp...
[OK] yt-dlp found
...

[3/5] Checking VLC...
[OK] VLC found
...

[4/5] Checking mpv...
[WARN] mpv not found (optional)...

[5/5] Checking Python dependencies...
[OK] textual installed
[OK] rich installed
[OK] requests installed
[OK] platformdirs installed

Summary
Status: [OK] All dependencies are installed
```

### Test Application

#### Test 1: Start Application

```powershell
# From source
python yt-x.py

# Using batch
.\yt-x.bat

# Using EXE
.\dist\yt-x.exe
```

**Checklist**:
- [ ] Application starts without errors
- [ ] Main menu appears
- [ ] Can navigate with keyboard
- [ ] Text is readable
- [ ] Colors are correct

#### Test 2: YouTube Browsing

**Steps**:
1. Select "Search"
2. Enter search query
3. Wait for results
4. Select a video

**Checklist**:
- [ ] Search returns results
- [ ] Video list displays correctly
- [ ] Titles, channels, durations show correctly
- [ ] Can select video

#### Test 3: Video Playback (VLC)

**Steps**:
1. Select video
2. Choose "Watch" or "Listen"

**Checklist**:
- [ ] VLC opens immediately
- [ ] Video plays
- [ ] No errors in VLC
- [ ] Deep link resolution works (yt-dlp → direct stream)
- [ ] m3u8 playlists work

#### Test 4: Audio Mode

**Steps**:
1. Select video
2. Choose "Listen (Audio Only)"

**Checklist**:
- [ ] VLC opens with audio only
- [ ] No video displayed
- [ ] Audio plays correctly

#### Test 5: Save Videos

**Steps**:
1. Select video
2. Choose "Save Video"
3. Go to "Saved Videos"

**Checklist**:
- [ ] Video appears in saved list
- [ ] Can play saved video
- [ ] Save persists across restarts

#### Test 6: Downloads

**Steps**:
1. Select video
2. Choose "Download"

**Checklist**:
- [ ] Download starts
- [ ] File saves to correct location
- [ ] File plays correctly
- [ ] Audio download works

---

## Deployment

### For Users: Distribution

#### Method 1: Pre-built EXE

1. Build EXE using stable Python (3.8-3.14)
2. Test EXE thoroughly
3. Upload to GitHub releases

```powershell
# Build
.\build-pyinstaller.bat

# Test
.\dist\yt-x.exe

# Release
# Go to: https://github.com/thepinak503/yt-x/releases/new
```

#### Method 2: Installer Package

Package `install.bat`, `yt-x.bat`, and `yt-x.exe` in a ZIP file.

### For Developers: Code Management

#### Commit Changes

```powershell
git add .
git commit -m "description of changes"
git push origin main
```

#### Create Branch

```powershell
git checkout -b feature-name
# Make changes
git add .
git commit -m "add feature"
git push -u origin feature-name
```

#### Merge to Main

```powershell
git checkout main
git merge feature-name
git push origin main
```

### For LLM/AI: Automated Tasks

#### Task 1: Update Code

```bash
# Modify files in yt_x/ directory
# Update app.py, config.py, player.py, etc.
```

#### Task 2: Test Changes

```bash
cd yt-x
python yt-x.py
# Test modified functionality
```

#### Task 3: Commit

```bash
git add .
git commit -m "description of changes"
git push origin main
```

#### Task 4: Build EXE

```bash
cd yt-x
.\build-pyinstaller.bat
```

#### Task 5: Test EXE

```bash
cd yt-x
.\dist\yt-x.exe
# Test all features
```

---

## Troubleshooting

### Application Won't Start

**Symptoms**:
- Nothing happens when running
- "module not found" error
- "ImportError"

**Solutions**:

1. Check Python version:
```powershell
python --version
# Should be 3.8-3.14
```

2. Install dependencies:
```powershell
pip install -r requirements.txt
```

3. Check yt-dlp:
```powershell
yt-dlp --version
# If not found: winget install yt-dlp
```

### VLC Won't Play Video

**Symptoms**:
- VLC opens but video doesn't play
- "network error" in VLC

**Solutions**:

1. Check yt-dlp is working:
```powershell
yt-dlp "VIDEO_URL" --get-url
# Should return direct stream URL
```

2. Test VLC directly:
```powershell
vlc "DIRECT_STREAM_URL"
```

3. Check network connection

### m3u8 Playlist Not Working

**Symptoms**:
- VLC doesn't load playlist
- Only first video plays

**Solutions**:

1. Check temporary directory exists:
```powershell
# Check: %TEMP%\yt-x
dir %TEMP%\yt-x
```

2. Check playlist file format:
```powershell
# Should be:
#EXTM3U
#EXTINF:-1,Video Title
URL
```

3. Verify VLC supports m3u8:
```powershell
vlc --version
# VLC 2.0+ required for best m3u8 support
```

### Build Failures

#### PyInstaller Error: "ModuleNotFoundError: No module named 'imp'"

**Cause**: Python 3.15+ incompatibility

**Solution**:
```powershell
# Use Python 3.8-3.14
winget install Python.Python.3.10
```

#### Nuitka Error: "cffi build failed"

**Cause**: Missing C compiler

**Solution**:
```powershell
winget install Microsoft.VisualStudio.2022.BuildTools
```

---

## Memory Snapshot

### Project Structure

```
yt-x/
├── yt_x/                    # Main Python package
│   ├── __init__.py          # Package initialization (v1.0.0)
│   ├── app.py                # Main application (Textual TUI)
│   ├── config.py             # Configuration manager
│   ├── ytdlp.py              # YouTube data fetcher (yt-dlp wrapper)
│   ├── player.py             # Video player (VLC/mpv with m3u8 support)
│   └── tui.py                # Terminal UI screens
├── yt-x.py                    # Entry point (CLI + TUI)
├── yt-x.bat                   # Portable launcher
├── install.bat                 # Full installer (with dependencies)
├── uninstall.bat               # Uninstaller
├── build-pyinstaller.bat      # PyInstaller build script
├── build.bat                 # Nuitka build script
├── test-deps.bat              # Dependency checker
├── setup.py                   # pip package setup
├── requirements.txt            # Python dependencies (min: 3.8)
├── README.md                  # User documentation
├── INSTRUCTIONS.md            # This file
├── BUILD_INSTRUCTIONS.md     # Detailed build guide
├── BUILD_STATUS.md           # Build status
├── RELEASE_SUMMARY.md       # Release preparation
└── LICENSE                   # MIT License
```

### Key Features Implemented

| Feature | Status | File | Notes |
|---------|--------|-------|-------|
| Modern TUI | ✅ | `app.py`, `tui.py` | Textual framework |
| YouTube browsing | ✅ | `tui.py` | Feed, trending, playlists |
| Search | ✅ | `tui.py` | With filters |
| Save videos | ✅ | `config.py` | Persistent storage |
| Recent tracking | ✅ | `config.py` | View history |
| Audio mode | ✅ | `player.py` | No video playback |
| Downloads | ✅ | `ytdlp.py` | Video and audio |
| VLC support | ✅ | `player.py` | m3u8 playlists |
| Deep link resolution | ✅ | `player.py` | yt-dlp backend |
| Windows paths | ✅ | `config.py` | %APPDATA%, %USERPROFILE% |
| Auto installer | ✅ | `install.bat` | Full setup |
| Uninstaller | ✅ | `uninstall.bat` | Clean removal |
| Dependency checker | ✅ | `test-deps.bat` | Verify setup |

### Python Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| textual | 7.3.0+ | TUI framework |
| rich | 14.2.0+ | Terminal formatting |
| requests | 2.32.0+ | HTTP requests |
| platformdirs | 4.5.0+ | Cross-platform paths |

### External Dependencies

| Tool | Required | Purpose | Install Command |
|-------|----------|---------|-----------------|
| Python | Yes | Runtime | `winget install Python.Python.3.10` |
| yt-dlp | Yes | YouTube data | `winget install yt-dlp` |
| VLC | Recommended | Video playback | `winget install VideoLAN.VLC` |
| mpv | Optional | Alternative player | `winget install mpv-player.mpv` |

### Build Tools

| Tool | Support Status | Notes |
|-------|----------------|-------|
| PyInstaller | ✅ 3.8-3.14 | Recommended |
| Nuitka | ⚠️ 3.8-3.14 | Advanced, requires C compiler |
| Python 3.15+ | ❌ | Not fully supported |

### Configuration

**Config File Location**:
- `%APPDATA%\yt-x\config.json`

**Default Config**:
```json
{
  "PLAYER": "mpv",
  "VIDEO_QUALITY": 1080,
  "DOWNLOAD_DIRECTORY": "%USERPROFILE%\\Videos\\yt-x",
  "ENABLE_PREVIEW": false,
  "SEARCH_HISTORY": true,
  "UPDATE_RECENT": true,
  "NO_OF_RECENT": 30,
  "DISOWN_STREAMING_PROCESS": true
}
```

**Cache Locations**:
- Config: `%APPDATA%\yt-x\`
- Cache: `%LOCALAPPDATA%\yt-x\`
- Data: `%LOCALAPPDATA%\yt-x\`
- Temp: `%TEMP%\yt-x\`

---

## Quick Reference for LLM/AI

### To Update Code

```bash
# 1. Edit files
# Edit files in yt_x/ directory

# 2. Test
cd yt-x && python yt-x.py

# 3. Commit
git add . && git commit -m "update" && git push
```

### To Build EXE

```bash
# 1. Install build tools
cd yt-x && pip install pyinstaller

# 2. Build
.\build-pyinstaller.bat

# 3. Test
.\dist\yt-x.exe

# 4. Test all features manually
```

### To Deploy

```bash
# 1. Commit all changes
cd yt-x && git add . && git commit -m "release v1.0.0"

# 2. Push
git push origin main

# 3. Create release on GitHub
# Go to: https://github.com/thepinak503/yt-x/releases/new
# Tag: v1.0.0
# Upload dist/yt-x.exe
```

### To Install (User)

```powershell
# Option 1: Full installer
.\install.bat

# Option 2: Portable
.\yt-x.bat

# Option 3: Python
python yt-x.py

# Option 4: EXE
.\dist\yt-x.exe
```

### To Uninstall

```powershell
# Run uninstaller
.\uninstall.bat

# Or manually:
# 1. Delete installation directory
# 2. Remove from PATH
# 3. Delete shortcuts
```

---

## Current Status

| Item | Status |
|-------|--------|
| Core Application | ✅ Complete |
| VLC m3u8 Support | ✅ Complete |
| Installer | ✅ Complete |
| Uninstaller | ✅ Complete |
| Documentation | ✅ Complete |
| Build Scripts | ✅ Complete |
| Git Repository | ✅ Pushed |
| EXE Build | ⚠️ Pending (requires Python 3.8-3.14) |

---

## Next Steps for LLM/AI

### Immediate Tasks

1. **Build EXE** (using Python 3.8-3.14):
   ```powershell
   cd yt-x
   .\build-pyinstaller.bat
   ```

2. **Test EXE** thoroughly:
   ```powershell
   .\dist\yt-x.exe
   # Test all features from "Testing" section
   ```

3. **Create GitHub Release**:
   - Tag: `v1.0.0`
   - Title: `yt-x v1.0.0`
   - Upload `dist/yt-x.exe`
   - Add release notes from this file

### Future Enhancements

1. **Add more video sites**: Support beyond YouTube (using yt-dlp)
2. **Enhanced TUI**: Add image previews, keyboard shortcuts
3. **Configuration UI**: In-app configuration editor
4. **Update checker**: Auto-check for updates
5. **Theme support**: Custom colors and themes

---

## Repository Information

- **Repository**: https://github.com/thepinak503/yt-x
- **Owner**: thepinak503
- **License**: MIT
- **Version**: 1.0.0
- **Python**: 3.8-3.14 (3.10+ recommended)

---

**End of INSTRUCTIONS.md**

This document contains all necessary information for:
- ✅ Users to install and use yt-x
- ✅ Developers to build and modify yt-x
- ✅ LLM/AI to automate tasks
- ✅ Troubleshooting common issues
- ✅ Complete memory snapshot of project

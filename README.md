# yt-x - YouTube Terminal Browser (Windows Native)

A modern, Windows-native terminal application for browsing YouTube and other yt-dlp supported sites.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## Features

- 🎬 **Modern TUI** - Beautiful terminal interface using Textual
- 📺 **YouTube Browsing** - Browse your feed, trending, subscriptions, playlists
- 🔍 **Search** - Search YouTube with filters
- 💾 **Save & Recent** - Save videos and track viewing history
- 🎵 **Audio Mode** - Listen to audio only
- 📥 **Downloads** - Download videos and audio
- 🔗 **Browser Integration** - Open videos in your browser
- ⚙️ **Configurable** - Customize everything
- 🎨 **Windows Native** - Built specifically for Windows

## Installation

### Prerequisites

Install the following dependencies:

1. **yt-dlp** (Required)
   ```powershell
   # Using winget
   winget install yt-dlp

   # Or download from https://github.com/yt-dlp/yt-dlp/releases
   ```

2. **Video Player** (Optional but recommended)
   - **mpv**: `winget install mpv-player.mpv`
   - **VLC**: `winget install VideoLAN.VLC`

3. **Python** (Required)
   - Python 3.8 or higher
   - Download from https://python.org

### Installing yt-x

#### Option 1: Using pip (Recommended)

```powershell
# Install from pip
pip install yt-x

# Run
yt-x
```

#### Option 2: From Source

```powershell
# Clone the repository
git clone https://github.com/pinakdhabu/yt-x.git
cd yt-x

# Install dependencies
pip install -r requirements.txt

# Run
python yt-x.py
```

#### Option 3: Compiled EXE

Download the pre-compiled EXE from the [Releases](https://github.com/pinakdhabu/yt-x/releases) page.

## Usage

### Interactive Mode

Launch the application:

```powershell
yt-x
```

### Command Line Options

```powershell
# Search YouTube
yt-x -s "search query"

# Open specific URL
yt-x -u "https://www.youtube.com/watch?v=..."

# Edit configuration
yt-x -c

# Show version
yt-x -v

# Show help
yt-x -h

# Check dependencies
yt-x deps
```

## Configuration

The configuration file is located at:
```
%APPDATA%\yt-x\config.json
```

### Configuration Options

```json
{
  "PLAYER": "mpv",
  "VIDEO_QUALITY": 1080,
  "DOWNLOAD_DIRECTORY": "%USERPROFILE%\\Videos\\yt-x",
  "PREFERRED_BROWSER": "chrome",
  "ENABLE_PREVIEW": false,
  "SEARCH_HISTORY": true,
  "UPDATE_RECENT": true,
  "NO_OF_RECENT": 30,
  "DISOWN_STREAMING_PROCESS": true,
  "NOTIFICATION_DURATION": 5,
  "WELCOME_SCREEN": true,
  "UPDATE_CHECK": true
}
```

## Key Features

### Main Menu

- **Your Feed** - Browse your YouTube feed
- **Trending** - See what's trending
- **Playlists** - Access your playlists
- **Search** - Search YouTube
- **Watch Later** - Your watch later list
- **Subscription Feed** - Latest from subscriptions
- **Channels** - Browse subscribed channels
- **Custom Playlists** - Your custom playlists
- **Liked Videos** - Videos you've liked
- **Saved Videos** - Videos you've saved
- **Watch History** - Your viewing history
- **Clips** - Browse clips
- **Edit Config** - Modify settings
- **Miscellaneous** - Additional options

### Video Actions

For each video, you can:
- **Watch** - Play video in mpv/VLC
- **Listen** - Play audio only
- **Save** - Save to saved videos
- **Open in Browser** - Open in default browser
- **Download** - Download video
- **Download Audio** - Download audio only

### Keyboard Shortcuts

- `q` - Quit / Go back
- `Enter` - Select
- `Esc` - Cancel / Go back
- `Ctrl+C` - Quit application

## Building from Source

### Compile to EXE

```powershell
# Install Nuitka
pip install Nuitka

# Compile (single file)
python -m nuitka --standalone --onefile --windows-disable-console yt-x.py

# The EXE will be created in the dist folder
```

Or use the provided build script:

```powershell
.\build.bat
```

## Development

### Setup Development Environment

```powershell
# Clone repository
git clone https://github.com/pinakdhabu/yt-x.git
cd yt-x

# Install in development mode
pip install -e .

# Run
yt-x
```

### Project Structure

```
yt-x/
├── yt_x/
│   ├── __init__.py      # Package init
│   ├── app.py          # Main application
│   ├── config.py       # Configuration management
│   ├── ytdlp.py       # yt-dlp wrapper
│   ├── player.py       # Video player wrapper
│   └── tui.py         # Terminal UI screens
├── yt-x.py           # Entry point
├── requirements.txt    # Python dependencies
├── setup.py          # Package setup
└── README.md         # This file
```

## Dependencies

### Required
- **Python** 3.8+
- **yt-dlp** - YouTube data extraction

### Python Dependencies
- **textual** - Modern Terminal UI
- **rich** - Terminal formatting
- **requests** - HTTP requests
- **platformdirs** - Cross-platform paths

### Optional
- **mpv** - Video player (recommended)
- **VLC** - Alternative video player
- **jq** - JSON processing

## Troubleshooting

### yt-dlp not found

Install yt-dlp:
```powershell
winget install yt-dlp
```

Or download from: https://github.com/yt-dlp/yt-dlp/releases

### Video won't play

Check that mpv or VLC is installed:
```powershell
mpv --version
vlc --version
```

### Configuration file issues

If configuration is corrupted, delete the config folder and restart:
```powershell
rm -r "$env:APPDATA\yt-x"
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

- Original yt-x by [Benexl](https://github.com/Benex254/yt-x)
- Windows native version by [pinakdhabu](https://github.com/pinakdhabu/yt-x)

## Support

For issues and feature requests:
- [GitHub Issues](https://github.com/pinakdhabu/yt-x/issues)
- [Discord](https://discord.gg/HBEmAwvbHV)

## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube data extraction
- [textual](https://github.com/Textualize/textual) - Terminal UI framework
- [mpv](https://mpv.io/) - Video player

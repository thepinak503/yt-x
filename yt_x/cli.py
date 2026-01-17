"""
yt-x - YouTube Terminal Browser (Windows Native)
Main entry point
"""

import sys
import webbrowser
from pathlib import Path

from .app import YTXApp


def print_header():
    """Print application header"""
    print("""
╔══════════════════════════════════════╗
║      YT-X - YouTube Terminal Browser      ║
║      v1.0.0 - Windows Native          ║
║      Copyright © 2024 pinakdhabu         ║
╚══════════════════════════════════════╝
    """)


def print_usage():
    """Print usage information"""
    print_header()
    print("""
Usage: yt-x [options]

Options:
  -s, --search <query>    Search YouTube directly
  -u, --url <url>        Open specific URL
  -c, --config            Edit configuration file
  -v, --version           Show version information
  -h, --help              Show this help message

Examples:
  yt-x                    Launch interactive UI
  yt-x -s "funny cats"  Search for funny cats
  yt-x -u <url>          Open specific video/playlist

For more information, visit: https://github.com/pinakdhabu/yt-x
    """)


def check_dependencies():
    """Check if required dependencies are installed"""
    import subprocess

    print("Checking dependencies...")

    # Check yt-dlp
    try:
        result = subprocess.run(
            ["yt-dlp", "--version"],
            capture_output=True,
            text=True,
            shell=True
        )
        if result.returncode == 0:
            print("  ✓ yt-dlp found")
        else:
            print("  ✗ yt-dlp not found")
            return False
    except:
        print("  ✗ yt-dlp not found")
        return False

    # Check jq
    try:
        result = subprocess.run(
            ["jq", "--version"],
            capture_output=True,
            text=True,
            shell=True
        )
        if result.returncode == 0:
            print("  ✓ jq found")
        else:
            print("  ! jq not found (optional)")
    except:
        print("  ! jq not found (optional)")

    # Check fzf
    try:
        result = subprocess.run(
            ["fzf", "--version"],
            capture_output=True,
            text=True,
            shell=True
        )
        if result.returncode == 0:
            print("  ✓ fzf found")
        else:
            print("  ! fzf not found (optional)")
    except:
        print("  ! fzf not found (optional)")

    # Check mpv
    try:
        result = subprocess.run(
            ["mpv", "--version"],
            capture_output=True,
            text=True,
            shell=True
        )
        if result.returncode == 0:
            print("  ✓ mpv found")
        else:
            print("  ! mpv not found (optional)")
    except:
        print("  ! mpv not found (optional)")

    # Check vlc
    try:
        result = subprocess.run(
            ["vlc", "--version"],
            capture_output=True,
            text=True,
            shell=True
        )
        if result.returncode == 0:
            print("  ✓ vlc found")
        else:
            print("  ! vlc not found (optional)")
    except:
        print("  ! vlc not found (optional)")

    print("\nRequired: yt-dlp")
    print("Optional: jq, fzf, mpv, vlc")
    print("")

    return True


def edit_config():
    """Open configuration file in editor"""
    from .config import Config

    config = Config()

    # Try to open in default editor
    import subprocess
    import os

    editor = config.get("PREFERRED_EDITOR", "notepad")

    try:
        subprocess.Popen(
            [editor, str(config.config_file)],
            shell=True
        )
        print(f"Opening config file: {config.config_file}")
    except Exception as e:
        print(f"Error opening config: {e}")


def direct_search(query: str):
    """Perform direct search and open first result"""
    from .config import Config
    from .ytdlp import YTDLP

    config = Config()
    ytdlp = YTDLP(config)

    print(f"Searching for: {query}")

    results = ytdlp.search(query, max_results=1)

    if results and len(results) > 0:
        video = results[0]
        url = video.get("url")

        print(f"Found: {video.get('title', 'Unknown')}")
        print(f"URL: {url}")

        # Ask to play
        response = input("Play this video? (y/n): ").strip().lower()
        if response == "y":
            from .player import Player
            player = Player(config)
            player.play_video(url)
    else:
        print("No results found")


def open_url(url: str):
    """Open specific URL"""
    print(f"Opening URL: {url}")
    webbrowser.open(url)


def main():
    """Main entry point"""
    import sys

    # Parse command line arguments
    args = sys.argv[1:]

    if len(args) == 0:
        # Launch GUI
        app = YTXApp()
        app.run()
    elif args[0] in ["-h", "--help"]:
        print_usage()
    elif args[0] in ["-v", "--version"]:
        from . import __version__
        print(f"yt-x v{__version__.__version__}")
        print(f"Copyright © 2024 {__version__.__author__}")
    elif args[0] in ["-c", "--config"]:
        edit_config()
    elif args[0] in ["-s", "--search"]:
        if len(args) > 1:
            query = " ".join(args[1:])
            direct_search(query)
        else:
            print("Error: Search query required")
            print_usage()
    elif args[0] in ["-u", "--url"]:
        if len(args) > 1:
            url = args[1]
            open_url(url)
        else:
            print("Error: URL required")
            print_usage()
    elif args[0] == "deps":
        check_dependencies()
    else:
        print(f"Unknown option: {args[0]}")
        print_usage()


if __name__ == "__main__":
    main()

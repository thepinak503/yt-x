"""
yt-x - Main entry point
"""

import sys
import subprocess

def check_dependencies():
    """Check if required dependencies are installed"""
    missing = []
    
    try:
        import textual
    except ImportError:
        missing.append("textual")
    
    try:
        import rich
    except ImportError:
        missing.append("rich")
    
    try:
        import requests
    except ImportError:
        missing.append("requests")
    
    try:
        import platformdirs
    except ImportError:
        missing.append("platformdirs")
    
    if missing:
        print("=" * 60)
        print("ERROR: Missing Python Dependencies")
        print("=" * 60)
        print()
        print("The following packages are required but not installed:")
        for pkg in missing:
            print(f"  - {pkg}")
        print()
        print("Please install them using:")
        print("  pip install -r requirements.txt")
        print()
        print("Or use the auto-installer:")
        print("  install.bat  (Batch)")
        print("  install.ps1 (PowerShell)")
        print()
        print("For quick install:")
        print("  irm https://raw.githubusercontent.com/thepinak503/yt-x/main/install.ps1 | iex")
        print()
        print("=" * 60)
        return False
    
    return True

def check_external_dependencies():
    """Check if external dependencies are installed"""
    external_missing = []
    
    try:
        result = subprocess.run(
            ["yt-dlp", "--version"],
            capture_output=True,
            text=True,
            shell=True
        )
        if result.returncode != 0:
            external_missing.append("yt-dlp")
    except:
        external_missing.append("yt-dlp")
    
    try:
        result = subprocess.run(
            ["vlc", "--version"],
            capture_output=True,
            text=True,
            shell=True
        )
        if result.returncode != 0:
            external_missing.append("vlc")
    except:
        pass
    
    try:
        result = subprocess.run(
            ["mpv", "--version"],
            capture_output=True,
            text=True,
            shell=True
        )
        if result.returncode != 0:
            external_missing.append("mpv")
    except:
        pass
    
    if external_missing:
        print("=" * 60)
        print("WARNING: External Dependencies Not Found")
        print("=" * 60)
        print()
        print("The following tools are recommended but not installed:")
        for tool in external_missing:
            print(f"  - {tool}")
        print()
        print("Install them using:")
        print("  winget install yt-dlp")
        print("  winget install VideoLAN.VLC")
        print("  winget install mpv-player.mpv")
        print()
        print("Or use the auto-installer:")
        print("  install.bat (requires admin)")
        print("  install.ps1")
        print("  irm https://raw.githubusercontent.com/thepinak503/yt-x/main/install.ps1 | iex")
        print()
        print("=" * 60)
    
    return len(external_missing) == 0

def main():
    """Main entry point with dependency checking"""
    print("Starting yt-x...")
    print()
    
    if not check_dependencies():
        sys.exit(1)
    
    check_external_dependencies()
    print()
    
    try:
        from yt_x.cli import main as cli_main
        cli_main()
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(0)
    except Exception as e:
        print("=" * 60)
        print("FATAL ERROR")
        print("=" * 60)
        print(f"An unexpected error occurred: {type(e).__name__}")
        print(f"Error: {e}")
        print()
        print("Please report this issue at:")
        print("https://github.com/thepinak503/yt-x/issues")
        print("=" * 60)
        sys.exit(1)

if __name__ == "__main__":
    main()

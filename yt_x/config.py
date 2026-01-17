"""
Configuration management for yt-x
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
from platformdirs import PlatformDirs


class Config:
    """Manages application configuration for yt-x"""

    def __init__(self):
        self.dirs = PlatformDirs(appname="yt-x", appauthor="pinakdhabu")
        self.config_dir = Path(self.dirs.user_config_dir)
        self.cache_dir = Path(self.dirs.user_cache_dir)
        self.data_dir = Path(self.dirs.user_data_dir)

        # Ensure directories exist
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Config file paths
        self.config_file = self.config_dir / "config.json"
        self.search_history_file = self.cache_dir / "search_history.txt"
        self.saved_videos_file = self.data_dir / "saved_videos.json"
        self.recent_videos_file = self.data_dir / "recent.json"
        self.custom_playlists_file = self.data_dir / "custom_playlists.json"
        self.subscriptions_file = self.data_dir / "subscriptions.json"
        self.custom_commands_file = self.data_dir / "custom_commands.json"

        # Default configuration
        self.defaults = {
            "PRETTY_PRINT": True,
            "IMAGE_RENDERER": "chafa",
            "DISOWN_STREAMING_PROCESS": True,
            "PREFERRED_EDITOR": "notepad",
            "PREFERRED_SELECTOR": "fzf",
            "VIDEO_QUALITY": 1080,
            "ENABLE_PREVIEW": False,
            "UPDATE_RECENT": True,
            "SEARCH_HISTORY": True,
            "NO_OF_RECENT": 30,
            "PLAYER": "mpv",
            "PREFERRED_BROWSER": "chrome",
            "NO_OF_SEARCH_RESULTS": 30,
            "NOTIFICATION_DURATION": 5,
            "DOWNLOAD_DIRECTORY": str(Path.home() / "Videos" / "yt-x"),
            "UPDATE_CHECK": True,
            "WELCOME_SCREEN": True,
            "ROFI_THEME": "",
            "AUTO_LOADED_EXTENSIONS": "",
        }

        self.config: Dict[str, Any] = {}
        self.load()

    def load(self):
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    self.config = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.config = {}
        else:
            self.config = {}

        # Merge with defaults
        for key, value in self.defaults.items():
            if key not in self.config:
                self.config[key] = value

        # Ensure download directory exists
        download_dir = Path(self.config["DOWNLOAD_DIRECTORY"])
        download_dir.mkdir(parents=True, exist_ok=True)

    def save(self):
        """Save configuration to file"""
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=2)

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default if default is not None else self.defaults.get(key))

    def set(self, key: str, value: Any):
        """Set configuration value"""
        self.config[key] = value
        self.save()

    def get_search_history(self) -> list[str]:
        """Get search history"""
        if not self.search_history_file.exists():
            return []
        try:
            with open(self.search_history_file, "r", encoding="utf-8") as f:
                return [line.strip() for line in f.readlines() if line.strip()]
        except IOError:
            return []

    def add_search_history(self, query: str):
        """Add query to search history"""
        if not self.get("SEARCH_HISTORY", True):
            return

        history = self.get_search_history()
        if query in history:
            history.remove(query)
        history.insert(0, query)

        # Keep only last 50 entries
        history = history[:50]

        with open(self.search_history_file, "w", encoding="utf-8") as f:
            f.write("\n".join(history))

    def clear_search_history(self):
        """Clear search history"""
        if self.search_history_file.exists():
            self.search_history_file.unlink()

    def get_saved_videos(self) -> list[Dict]:
        """Get saved videos"""
        if not self.saved_videos_file.exists():
            return []
        try:
            with open(self.saved_videos_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("entries", [])
        except (json.JSONDecodeError, IOError):
            return []

    def add_saved_video(self, video: Dict):
        """Add video to saved videos"""
        saved = self.get_saved_videos()
        video_id = video.get("id")

        # Remove if already exists
        saved = [v for v in saved if v.get("id") != video_id]

        # Add to beginning
        saved.insert(0, video)

        # Keep only configured number
        no_of_recent = self.get("NO_OF_RECENT", 30)
        saved = saved[:no_of_recent]

        with open(self.saved_videos_file, "w", encoding="utf-8") as f:
            json.dump({"entries": saved}, f, indent=2)

    def remove_saved_video(self, video_id: str):
        """Remove video from saved videos"""
        saved = self.get_saved_videos()
        saved = [v for v in saved if v.get("id") != video_id]

        with open(self.saved_videos_file, "w", encoding="utf-8") as f:
            json.dump({"entries": saved}, f, indent=2)

    def get_recent_videos(self) -> list[Dict]:
        """Get recent videos"""
        if not self.recent_videos_file.exists():
            return []
        try:
            with open(self.recent_videos_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("entries", [])
        except (json.JSONDecodeError, IOError):
            return []

    def add_recent_video(self, video: Dict):
        """Add video to recent"""
        if not self.get("UPDATE_RECENT", True):
            return

        recent = self.get_recent_videos()
        video_id = video.get("id")

        # Remove if already exists
        recent = [v for v in recent if v.get("id") != video_id]

        # Add to beginning
        recent.insert(0, video)

        # Keep only configured number
        no_of_recent = self.get("NO_OF_RECENT", 30)
        recent = recent[:no_of_recent]

        with open(self.recent_videos_file, "w", encoding="utf-8") as f:
            json.dump({"entries": recent}, f, indent=2)

    def get_custom_playlists(self) -> list[Dict]:
        """Get custom playlists"""
        if not self.custom_playlists_file.exists():
            return []
        try:
            with open(self.custom_playlists_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def add_custom_playlist(self, name: str, playlist_url: str, playlist_watch_url: str):
        """Add custom playlist"""
        playlists = self.get_custom_playlists()
        playlist = {
            "name": name,
            "playlistUrl": playlist_url,
            "playlistWatchUrl": playlist_watch_url,
        }
        playlists.append(playlist)

        with open(self.custom_playlists_file, "w", encoding="utf-8") as f:
            json.dump(playlists, f, indent=2)

    def get_subscriptions(self) -> list[Dict]:
        """Get subscriptions"""
        if not self.subscriptions_file.exists():
            return []
        try:
            with open(self.subscriptions_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("entries", [])
        except (json.JSONDecodeError, IOError):
            return []

    def save_subscriptions(self, entries: list[Dict]):
        """Save subscriptions"""
        with open(self.subscriptions_file, "w", encoding="utf-8") as f:
            json.dump({"entries": entries}, f, indent=2)

    def add_subscription(self, channel: Dict):
        """Add channel to subscriptions"""
        subs = self.get_subscriptions()
        channel_id = channel.get("id")

        # Remove if already exists
        subs = [c for c in subs if c.get("id") != channel_id]

        # Add to beginning
        subs.insert(0, channel)

        with open(self.subscriptions_file, "w", encoding="utf-8") as f:
            json.dump({"entries": subs}, f, indent=2)

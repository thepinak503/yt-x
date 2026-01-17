"""
Main application class
"""

from textual.app import App, ComposeResult
from textual.screen import Screen

from .config import Config
from .ytdlp import YTDLP
from .player import Player
from .tui import (
    MainScreen,
    VideoListScreen,
    VideoActionsScreen,
    SearchScreen,
    SavedVideosScreen,
    CustomPlaylistsScreen,
    ChannelsScreen,
    ConfigScreen,
    MiscScreen,
)


class YTXApp(App):
    """Main YTX Application"""

    CSS = """
    Screen {
        background: $background;
    }

    Header {
        background: $panel;
        text-style: bold;
    }

    Footer {
        background: $panel;
        text-style: bold;
    }

    Button {
        width: 100%;
    }

    DataTable {
        height: 30;
    }

    Static {
        margin: 1;
    }

    #screen-title {
        text-align: center;
        text-style: bold;
        color: $accent;
        margin: 1;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("ctrl+c", "quit", "Quit"),
    ]

    SCREENS = {
        "main": MainScreen,
        "video_list": VideoListScreen,
        "video_actions": VideoActionsScreen,
        "search": SearchScreen,
        "saved": SavedVideosScreen,
        "custom_playlists": CustomPlaylistsScreen,
        "channels": ChannelsScreen,
        "config": ConfigScreen,
        "misc": MiscScreen,
    }

    def __init__(self):
        super().__init__()
        self.config = Config()
        self.ytdlp = YTDLP(self.config)
        self.player = Player(self.config, ytdlp_instance=self.ytdlp)

    def on_mount(self) -> None:
        self.push_screen("main")

    def fetch_videos(self, url: str) -> list:
        """Fetch videos from URL"""
        data = self.ytdlp.fetch_json(url)
        if data:
            return data.get("entries", [])
        return []

    def open_search_screen(self, title: str, url: str):
        """Open screen showing video list"""
        screen = VideoListScreen(self, title, url)
        self.push_screen(screen)

    def open_video_actions(self, video: dict):
        """Open video actions screen"""
        screen = VideoActionsScreen(self, video)
        self.push_screen(screen)

    def action_quit(self) -> None:
        """Quit the application"""
        self.exit()

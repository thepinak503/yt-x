"""
Main TUI application for yt-x
"""

from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.binding import Binding
from textual.reactive import reactive
import webbrowser
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .app import YTXApp


class MainScreen(Screen):
    """Main screen with action menu"""

    CSS = """
    MainScreen {
        align: center middle;
    }

    #action-menu {
        width: 60;
        height: 40;
        border: thick $primary;
    }

    Button {
        margin: 1;
    }

    .category {
        text-style: bold;
        color: $accent;
    }
    """

    def __init__(self, app):
        super().__init__()
        self.app_ref = app

    def compose(self):
        with Vertical(id="main-container"):
            yield Static(
                "[bold cyan]╔══════════════════════════════════════╗[/bold cyan]\n"
                "[bold cyan]║       [white]YT-X [cyan]- YouTube Terminal Browser   [cyan]║[/bold cyan]\n"
                "[bold cyan]║       [white]v1.0.0 [cyan]- Windows Native      [cyan]║[/bold cyan]\n"
                "[bold cyan]╚══════════════════════════════════════╝[/bold cyan]",
                id="header"
            )
            with Vertical(id="action-menu"):
                yield Button("Your Feed", id="feed")
                yield Button("Trending", id="trending")
                yield Button("Playlists", id="playlists")
                yield Button("Search", id="search")
                yield Button("Watch Later", id="watch-later")
                yield Button("Subscription Feed", id="subscriptions")
                yield Button("Channels", id="channels")
                yield Button("Custom Playlists", id="custom-playlists")
                yield Button("Liked Videos", id="liked")
                yield Button("Saved Videos", id="saved")
                yield Button("Watch History", id="history")
                yield Button("Clips", id="clips")
                yield Button("Edit Config", id="config")
                yield Button("Miscellaneous", id="misc")
                yield Button("Exit", id="exit", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id

        actions = {
            "feed": self.open_feed,
            "trending": self.open_trending,
            "playlists": self.open_playlists,
            "search": self.open_search,
            "watch-later": self.open_watch_later,
            "subscriptions": self.open_subscriptions,
            "channels": self.open_channels,
            "custom-playlists": self.open_custom_playlists,
            "liked": self.open_liked,
            "saved": self.open_saved,
            "history": self.open_history,
            "clips": self.open_clips,
            "config": self.open_config,
            "misc": self.open_misc,
            "exit": self.exit_app,
        }

        if button_id in actions:
            actions[button_id]()

    def open_feed(self):
        self.app_ref.open_search_screen("Your Feed", "https://www.youtube.com")

    def open_trending(self):
        self.app_ref.open_search_screen("Trending", "https://www.youtube.com/feed/trending")

    def open_playlists(self):
        self.app_ref.open_search_screen("Playlists", "https://www.youtube.com/feed/playlists")

    def open_search(self):
        self.app_ref.push_screen(SearchScreen(self.app_ref))

    def open_watch_later(self):
        self.app_ref.open_search_screen("Watch Later", "https://www.youtube.com/playlist?list=WL")

    def open_subscriptions(self):
        self.app_ref.open_search_screen("Subscription Feed", "https://www.youtube.com/feed/subscriptions")

    def open_channels(self):
        self.app_ref.push_screen(ChannelsScreen(self.app_ref))

    def open_custom_playlists(self):
        self.app_ref.push_screen(CustomPlaylistsScreen(self.app_ref))

    def open_liked(self):
        self.app_ref.open_search_screen("Liked Videos", "https://www.youtube.com/playlist?list=LL")

    def open_saved(self):
        self.app_ref.push_screen(SavedVideosScreen(self.app_ref))

    def open_history(self):
        self.app_ref.open_search_screen("Watch History", "https://www.youtube.com/feed/history")

    def open_clips(self):
        self.app_ref.open_search_screen("Clips", "https://www.youtube.com/feed/clips")

    def open_config(self):
        self.app_ref.push_screen(ConfigScreen(self.app_ref))

    def open_misc(self):
        self.app_ref.push_screen(MiscScreen(self.app_ref))

    def exit_app(self):
        self.app_ref.exit()


class VideoListScreen(Screen):
    """Screen showing a list of videos"""

    BINDINGS = [
        Binding("q", "pop_screen", "Back"),
        Binding("r", "refresh", "Refresh"),
        Binding("enter", "select_video", "Select"),
        Binding("escape", "pop_screen", "Back"),
    ]

    def __init__(self, app, title: str, url: str):
        super().__init__()
        self.app_ref = app
        self.title = title
        self.url = url
        self.videos = []
        self.selected_video = None

    def compose(self):
        yield Header()
        with Vertical():
            yield Static(f"[bold cyan]{self.title}[/bold cyan]", id="screen-title")
            yield DataTable(id="video-table")
        yield Footer()

    def on_mount(self) -> None:
        self.load_videos()

    def load_videos(self):
        table = self.query_one("#video-table", DataTable)
        table.clear()
        table.add_column("Title")
        table.add_column("Channel")
        table.add_column("Duration")
        table.add_column("Views")

        self.videos = self.app_ref.fetch_videos(self.url)

        for video in self.videos:
            title = video.get("title", "Unknown")[:60]
            channel = video.get("channel", "Unknown")[:25]
            duration = self._format_duration(video.get("duration", 0))
            views = self._format_views(video.get("view_count", 0))

            table.add_row(
                title,
                channel,
                duration,
                views
            )

    def _format_duration(self, duration: int) -> str:
        """Format duration in human readable format"""
        hours = duration // 3600
        minutes = (duration % 3600) // 60
        seconds = duration % 60

        if hours > 0:
            return f"{hours}h {minutes}m"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"

    def _format_views(self, views: int) -> str:
        """Format view count"""
        if views >= 1000000:
            return f"{views / 1000000:.1f}M"
        elif views >= 1000:
            return f"{views / 1000:.1f}K"
        else:
            return str(views)

    def action_select_video(self):
        table = self.query_one("#video-table", DataTable)
        row_key, _ = table.cursor_cell

        if row_key is not None and row_key in self.videos:
            video = self.videos[row_key]
            self.selected_video = video
            self.app.open_video_actions(video)

    def action_refresh(self):
        self.load_videos()


class SearchScreen(Screen):
    """Screen for searching YouTube"""

    BINDINGS = [
        Binding("escape", "pop_screen", "Cancel"),
        Binding("enter", "do_search", "Search"),
    ]

    def __init__(self, app):
        super().__init__()
        self.app_ref = app

    def compose(self):
        yield Header()
        with Vertical():
            yield Static("[bold cyan]Search YouTube[/bold cyan]")
            yield Input(placeholder="Enter search query...", id="search-input")
            yield Static("Press Enter to search, Escape to cancel", id="help-text")
        yield Footer()

    def on_mount(self) -> None:
        input_box = self.query_one("#search-input", Input)
        input_box.focus()

    def action_do_search(self):
        input_box = self.query_one("#search-input", Input)
        query = input_box.value.strip()

        if query:
            self.app_ref.config.add_search_history(query)
            # Encode query for URL
            import urllib.parse
            encoded_query = urllib.parse.quote(query)
            search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
            self.app_ref.open_search_screen(f"Search: {query}", search_url)
        else:
            self.pop_screen()


class SavedVideosScreen(Screen):
    """Screen showing saved videos"""

    BINDINGS = [
        Binding("q", "pop_screen", "Back"),
        Binding("d", "delete_video", "Delete"),
        Binding("escape", "pop_screen", "Back"),
    ]

    def __init__(self, app):
        super().__init__()
        self.app_ref = app

    def compose(self):
        yield Header()
        with Vertical():
            yield Static("[bold cyan]Saved Videos[/bold cyan]")
            yield DataTable(id="saved-table")
        yield Footer()

    def on_mount(self) -> None:
        self.load_saved_videos()

    def load_saved_videos(self):
        table = self.query_one("#saved-table", DataTable)
        table.clear()
        table.add_column("Title")
        table.add_column("Channel")

        saved = self.app_ref.config.get_saved_videos()

        for video in saved:
            title = video.get("title", "Unknown")[:60]
            channel = video.get("channel", "Unknown")[:25]
            table.add_row(title, channel)

    def action_delete_video(self):
        table = self.query_one("#saved-table", DataTable)
        row_key, _ = table.cursor_cell

        if row_key is not None:
            saved = self.app_ref.config.get_saved_videos()
            if row_key < len(saved):
                video_id = saved[row_key].get("id")
                self.app_ref.config.remove_saved_video(video_id)
                self.load_saved_videos()


class CustomPlaylistsScreen(Screen):
    """Screen for managing custom playlists"""

    BINDINGS = [
        Binding("q", "pop_screen", "Back"),
        Binding("a", "add_playlist", "Add"),
        Binding("escape", "pop_screen", "Back"),
    ]

    def __init__(self, app):
        super().__init__()
        self.app_ref = app

    def compose(self):
        yield Header()
        with Vertical():
            yield Static("[bold cyan]Custom Playlists[/bold cyan]")
            yield DataTable(id="playlist-table")
        yield Footer()

    def on_mount(self) -> None:
        self.load_playlists()

    def load_playlists(self):
        table = self.query_one("#playlist-table", DataTable)
        table.clear()
        table.add_column("Name")
        table.add_column("URL")

        playlists = self.app_ref.config.get_custom_playlists()

        for playlist in playlists:
            name = playlist.get("name", "Unknown")
            url = playlist.get("playlistUrl", "")[:40]
            table.add_row(name, url)


class ChannelsScreen(Screen):
    """Screen for browsing subscribed channels"""

    BINDINGS = [
        Binding("q", "pop_screen", "Back"),
        Binding("s", "sync_subscriptions", "Sync"),
        Binding("escape", "pop_screen", "Back"),
    ]

    def __init__(self, app):
        super().__init__()
        self.app_ref = app

    def compose(self):
        yield Header()
        with Vertical():
            yield Static("[bold cyan]Channels[/bold cyan]")
            yield DataTable(id="channel-table")
        yield Footer()

    def on_mount(self) -> None:
        self.load_channels()

    def load_channels(self):
        table = self.query_one("#channel-table", DataTable)
        table.clear()
        table.add_column("Channel")
        table.add_column("Subscribers")

        subs = self.app_ref.config.get_subscriptions()

        for channel in subs:
            name = channel.get("channel", "Unknown")
            subs_count = channel.get("channel_follower_count", 0)
            table.add_row(name, str(subs_count))

    def action_sync_subscriptions(self):
        # Sync subscriptions from YouTube
        pass


class ConfigScreen(Screen):
    """Screen for editing configuration"""

    BINDINGS = [
        Binding("q", "pop_screen", "Back"),
        Binding("s", "save", "Save"),
        Binding("escape", "pop_screen", "Cancel"),
    ]

    def __init__(self, app):
        super().__init__()
        self.app_ref = app

    def compose(self):
        yield Header()
        with Vertical():
            yield Static("[bold cyan]Configuration[/bold cyan]")
            yield Static("Configuration editor coming soon...")
        yield Footer()


class MiscScreen(Screen):
    """Screen for miscellaneous options"""

    def __init__(self, app):
        super().__init__()
        self.app_ref = app

    def compose(self):
        yield Header()
        with Vertical(id="misc-menu"):
            yield Static("[bold cyan]Miscellaneous[/bold cyan]")
            yield Button("Explore Channels", id="explore-channels")
            yield Button("Explore Playlists", id="explore-playlists")
            yield Button("Search History", id="search-history")
            yield Button("Clear Search History", id="clear-history")
            yield Button("Back", id="back")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id

        if button_id == "explore-channels":
            self.app.push_screen(ChannelsScreen(self.app_ref))
        elif button_id == "explore-playlists":
            self.app.push_screen(CustomPlaylistsScreen(self.app_ref))
        elif button_id == "search-history":
            # Show search history
            pass
        elif button_id == "clear-history":
            self.app_ref.config.clear_search_history()
        elif button_id == "back":
            self.pop_screen()


class VideoActionsScreen(Screen):
    """Screen with actions for a selected video"""

    def __init__(self, app, video: dict):
        super().__init__()
        self.app_ref = app
        self.video = video

    def compose(self):
        yield Header()
        with Vertical(id="video-actions"):
            yield Static("[bold cyan]Video Actions[/bold cyan]")
            yield Static(f"[bold]Title:[/bold] {self.video.get('title', 'Unknown')}")
            yield Static(f"[bold]Channel:[/bold] {self.video.get('channel', 'Unknown')}")
            yield Static("")
            yield Button("Watch", id="watch")
            yield Button("Listen (Audio Only)", id="listen")
            yield Button("Save Video", id="save")
            yield Button("Open in Browser", id="browser")
            yield Button("Download", id="download")
            yield Button("Download Audio Only", id="download-audio")
            yield Button("Back", id="back")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        video_url = self.video.get("url", "")

        if button_id == "watch":
            self.app_ref.player.play_video(video_url)
            self.app_ref.config.add_recent_video(self.video)
            self.pop_screen()
        elif button_id == "listen":
            self.app_ref.player.play_video(video_url, audio_only=True)
            self.app_ref.config.add_recent_video(self.video)
            self.pop_screen()
        elif button_id == "save":
            self.app_ref.config.add_saved_video(self.video)
            self.pop_screen()
        elif button_id == "browser":
            webbrowser.open(video_url)
        elif button_id == "download":
            output_template = str(
                Path(self.app_ref.config.get("DOWNLOAD_DIRECTORY")) / "videos" / "%(channel)s" / "%(title)s.%(ext)s"
            )
            self.app_ref.ytdlp.download(video_url, output_template)
        elif button_id == "download-audio":
            output_template = str(
                Path(self.app_ref.config.get("DOWNLOAD_DIRECTORY")) / "audio" / "%(channel)s" / "%(title)s.%(ext)s"
            )
            self.app_ref.ytdlp.download(video_url, output_template, audio_only=True)
        elif button_id == "back":
            self.pop_screen()

"""
Video player wrapper for mpv and vlc
Handles m3u8 playlists using yt-dlp for deep link resolution
"""

import subprocess
import tempfile
import os
from typing import Optional, Tuple
from pathlib import Path


class Player:
    """Wrapper for video players (mpv, vlc)"""

    def __init__(self, config, ytdlp_instance=None):
        self.config = config
        self.ytdlp = ytdlp_instance
        self.player_type = config.get("PLAYER", "mpv")
        self.player_cmd = self._find_player()
        self.temp_dir = Path(tempfile.gettempdir()) / "yt-x"
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def _find_player(self) -> str:
        """Find video player executable"""
        if self.player_type.lower() == "mpv":
            for cmd in ["mpv.exe", "mpv"]:
                try:
                    result = subprocess.run(
                        ["where", cmd],
                        capture_output=True,
                        text=True,
                        shell=True
                    )
                    if result.returncode == 0:
                        return cmd
                except:
                    pass
            return "mpv"

        elif self.player_type.lower() == "vlc":
            for cmd in ["vlc.exe", "vlc"]:
                try:
                    result = subprocess.run(
                        ["where", cmd],
                        capture_output=True,
                        text=True,
                        shell=True
                    )
                    if result.returncode == 0:
                        return cmd
                except:
                    pass
            return "vlc"

        return "mpv"

    def _resolve_with_ytdlp(self, url: str) -> Tuple[str, Optional[str]]:
        """
        Resolve video URL using yt-dlp to get direct stream

        Returns:
            Tuple of (url_to_play, playlist_file_path)
        """
        if not self.ytdlp:
            return url, None

        try:
            import json

            # Get direct stream URL from yt-dlp
            cmd = [
                self.ytdlp.yt_dlp_cmd,
                url,
                "--get-url",
                "--get-title",
                "--no-warnings",
                "-f", "best"
            ]

            # Add browser args
            cmd.extend(self.ytdlp._get_browser_args())

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                shell=True,
                timeout=30
            )

            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")
                # Last non-empty line is the URL
                url_lines = [l for l in lines if l.strip()]
                if url_lines:
                    return url_lines[-1].strip(), None

        except subprocess.TimeoutExpired:
            print("Timeout resolving video URL, trying direct playback")
        except Exception as e:
            print(f"Error resolving URL: {e}, trying direct playback")

        return url, None

    def _create_m3u8_playlist(self, video_urls: list, titles: list = None) -> str:
        """
        Create m3u8 playlist file for VLC

        Args:
            video_urls: List of video URLs
            titles: Optional list of video titles

        Returns:
            Path to m3u8 playlist file
        """
        playlist_path = self.temp_dir / f"playlist_{os.getpid()}.m3u8"

        with open(playlist_path, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")

            for i, url in enumerate(video_urls):
                if titles and i < len(titles):
                    title = titles[i]
                    f.write(f"#EXTINF:-1,{title}\n")
                f.write(f"{url}\n")

        return str(playlist_path)

    def _get_playlist_urls(self, playlist_url: str) -> Tuple[list, list]:
        """
        Get all video URLs from playlist using yt-dlp

        Returns:
            Tuple of (video_urls, titles)
        """
        if not self.ytdlp:
            return [playlist_url], []

        try:
            import json

            # Get playlist data
            data = self.ytdlp.fetch_json(playlist_url, flat=True)

            if not data or "entries" not in data:
                return [playlist_url], []

            entries = data["entries"]
            urls = [entry.get("url") or entry.get("webpage_url") for entry in entries if entry.get("url") or entry.get("webpage_url")]
            titles = [entry.get("title", "Unknown") for entry in entries]

            return urls, titles

        except Exception as e:
            print(f"Error getting playlist URLs: {e}")
            return [playlist_url], []

    def play_video(self, url: str, audio_only: bool = False, use_ytdlp: bool = True):
        """
        Play video URL - resolves deep link with yt-dlp

        Args:
            url: Video URL to play
            audio_only: Play audio only
            use_ytdlp: Whether to use yt-dlp to resolve URL
        """
        # Resolve URL with yt-dlp if enabled and using VLC
        resolved_url, playlist_file = url, None

        if use_ytdlp and self.player_type.lower() == "vlc":
            resolved_url, playlist_file = self._resolve_with_ytdlp(url)

        # Prepare VLC command
        if self.player_type.lower() == "vlc":
            cmd = [self.player_cmd]

            if audio_only:
                cmd.extend(["--no-video"])

            # If we have a playlist file, use it
            if playlist_file:
                cmd.append(playlist_file)
            else:
                cmd.append(resolved_url)
        else:
            # MPV can handle URLs directly
            cmd = [self.player_cmd]

            if audio_only:
                cmd.extend(["--no-video", "--force-window=no"])

            cmd.append(resolved_url)

        # Launch player
        try:
            if self.config.get("DISOWN_STREAMING_PROCESS", True):
                subprocess.Popen(
                    cmd,
                    shell=True,
                    creationflags=subprocess.DETACHED_PROCESS,
                    close_fds=True
                )
                print(f"Playing: {resolved_url[:80]}...")
            else:
                subprocess.run(cmd, shell=True)
        except Exception as e:
            print(f"Error playing video: {e}")

    def play_playlist(self, playlist_url: str, audio_only: bool = False):
        """
        Play playlist - creates m3u8 for VLC

        Args:
            playlist_url: Playlist URL
            audio_only: Play audio only
        """
        print("Loading playlist...")

        # Get all video URLs from playlist
        video_urls, titles = self._get_playlist_urls(playlist_url)

        if len(video_urls) == 1:
            # Single video, play directly
            self.play_video(video_urls[0], audio_only, use_ytdlp=True)
            return

        # Multiple videos - create m3u8 playlist
        print(f"Creating playlist with {len(video_urls)} videos...")

        if self.player_type.lower() == "vlc":
            # Create m3u8 playlist for VLC
            m3u8_path = self._create_m3u8_playlist(video_urls, titles)

            cmd = [self.player_cmd]

            if audio_only:
                cmd.extend(["--no-video"])

            cmd.append(m3u8_path)

            try:
                if self.config.get("DISOWN_STREAMING_PROCESS", True):
                    subprocess.Popen(
                        cmd,
                        shell=True,
                        creationflags=subprocess.DETACHED_PROCESS,
                        close_fds=True
                    )
                    print(f"Playing playlist with {len(video_urls)} videos in VLC")
                else:
                    subprocess.run(cmd, shell=True)
            except Exception as e:
                print(f"Error playing playlist: {e}")
        else:
            # MPV can handle playlists directly
            self.play_video(playlist_url, audio_only, use_ytdlp=False)

    def play_file(self, file_path: str, audio_only: bool = False):
        """
        Play local file

        Args:
            file_path: Path to video file
            audio_only: Play audio only
        """
        cmd = [self.player_cmd]

        if audio_only:
            cmd.extend(["--no-video", "--force-window=no"])

        cmd.append(str(file_path))

        try:
            if self.config.get("DISOWN_STREAMING_PROCESS", True):
                subprocess.Popen(
                    cmd,
                    shell=True,
                    creationflags=subprocess.DETACHED_PROCESS,
                    close_fds=True
                )
            else:
                subprocess.run(cmd, shell=True)
        except Exception as e:
            print(f"Error playing file: {e}")

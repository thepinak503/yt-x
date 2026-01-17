"""
Video player wrapper for mpv and vlc
"""

import subprocess
from typing import Optional


class Player:
    """Wrapper for video players (mpv, vlc)"""

    def __init__(self, config):
        self.config = config
        self.player_type = config.get("PLAYER", "mpv")
        self.player_cmd = self._find_player()

    def _find_player(self) -> str:
        """Find the video player executable"""
        if self.player_type.lower() == "mpv":
            # Try mpv.exe, mpv
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
            return "mpv"  # fallback

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
            return "vlc"  # fallback

        # Default to mpv
        return "mpv"

    def play_video(self, url: str, audio_only: bool = False):
        """
        Play video URL

        Args:
            url: Video URL to play
            audio_only: Play audio only (no video)
        """
        cmd = [self.player_cmd]

        if audio_only:
            cmd.extend(["--no-video", "--force-window=no"])

        cmd.append(url)

        try:
            if self.config.get("DISOWN_STREAMING_PROCESS", True):
                # Run in background
                subprocess.Popen(
                    cmd,
                    shell=True,
                    creationflags=subprocess.DETACHED_PROCESS
                )
            else:
                # Run in foreground
                subprocess.run(cmd, shell=True)
        except Exception as e:
            print(f"Error playing video: {e}")

    def play_playlist(self, playlist_url: str, audio_only: bool = False):
        """
        Play playlist URL

        Args:
            playlist_url: Playlist URL
            audio_only: Play audio only
        """
        self.play_video(playlist_url, audio_only)

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

        cmd.append(file_path)

        try:
            if self.config.get("DISOWN_STREAMING_PROCESS", True):
                subprocess.Popen(
                    cmd,
                    shell=True,
                    creationflags=subprocess.DETACHED_PROCESS
                )
            else:
                subprocess.run(cmd, shell=True)
        except Exception as e:
            print(f"Error playing file: {e}")

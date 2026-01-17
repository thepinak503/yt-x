"""
yt-dlp wrapper for fetching YouTube data
"""

import json
import subprocess
from pathlib import Path
from typing import Optional, Dict, List


class YTDLP:
    """Wrapper for yt-dlp command"""

    def __init__(self, config):
        self.config = config
        self.yt_dlp_cmd = self._find_yt_dlp()

    def _find_yt_dlp(self) -> str:
        """Find yt-dlp executable"""
        # Check common locations
        for cmd in ["yt-dlp", "yt-dlp.exe", "yt-dlp.bat"]:
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

        # Try to run directly
        for cmd in ["yt-dlp", "yt-dlp.exe"]:
            try:
                subprocess.run(
                    [cmd, "--version"],
                    capture_output=True,
                    check=False,
                    shell=True
                )
                return cmd
            except:
                pass

        raise RuntimeError(
            "yt-dlp not found. Please install it from https://github.com/yt-dlp/yt-dlp"
        )

    def _get_browser_args(self) -> List[str]:
        """Get browser arguments for yt-dlp"""
        browser = self.config.get("PREFERRED_BROWSER", "")
        if browser:
            return ["--cookies-from-browser", browser]
        return []

    def fetch_json(self, url: str, flat: bool = True, extra_args: Optional[List[str]] = None) -> Optional[Dict]:
        """
        Fetch JSON data from yt-dlp

        Args:
            url: URL to fetch
            flat: Use flat playlist
            extra_args: Additional arguments to pass to yt-dlp

        Returns:
            JSON data as dictionary
        """
        cmd = [self.yt_dlp_cmd, url, "-J"]

        if flat:
            cmd.append("--flat-playlist")

        # Add browser args
        cmd.extend(self._get_browser_args())

        # Add extra args
        if extra_args:
            cmd.extend(extra_args)

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                shell=True
            )

            if result.returncode != 0:
                print(f"Error fetching data: {result.stderr}")
                return None

            return json.loads(result.stdout)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

    def fetch_playlist(
        self,
        url: str,
        start: int = 1,
        end: Optional[int] = None,
        extra_args: Optional[List[str]] = None
    ) -> Optional[Dict]:
        """
        Fetch playlist data

        Args:
            url: Playlist URL
            start: Start index
            end: End index
            extra_args: Additional arguments

        Returns:
            JSON data with playlist entries
        """
        cmd = [self.yt_dlp_cmd, url, "-J", "--flat-playlist"]

        # Add browser args
        cmd.extend(self._get_browser_args())

        # Add playlist range
        cmd.extend(["--playlist-start", str(start)])
        if end:
            cmd.extend(["--playlist-end", str(end)])

        # Add extra args
        if extra_args:
            cmd.extend(extra_args)

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                shell=True
            )

            if result.returncode != 0:
                print(f"Error fetching playlist: {result.stderr}")
                return None

            data = json.loads(result.stdout)
            return data
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_video_url(self, url: str, quality: Optional[int] = None, audio_only: bool = False) -> Optional[str]:
        """
        Get direct video URL for streaming

        Args:
            url: Video URL
            quality: Maximum height (e.g., 1080 for 1080p)
            audio_only: Get audio URL only

        Returns:
            Direct URL to video stream
        """
        cmd = [self.yt_dlp_cmd, url, "--get-url", "--no-warnings"]

        if audio_only:
            cmd.extend(["-f", "bestaudio/best"])
        elif quality:
            cmd.extend(["-f", f"best[height<={quality}]/best"])
        else:
            cmd.extend(["-f", "best"])

        # Add browser args
        cmd.extend(self._get_browser_args())

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                shell=True
            )

            if result.returncode != 0:
                return None

            # Return the last line (best quality)
            urls = result.stdout.strip().split("\n")
            return urls[-1] if urls else None
        except Exception as e:
            print(f"Error getting video URL: {e}")
            return None

    def download(
        self,
        url: str,
        output_template: str,
        audio_only: bool = False,
        extra_args: Optional[List[str]] = None
    ) -> bool:
        """
        Download video/audio

        Args:
            url: URL to download
            output_template: Output filename template
            audio_only: Download audio only
            extra_args: Additional arguments

        Returns:
            True if successful
        """
        cmd = [self.yt_dlp_cmd, url, "-o", output_template]

        if audio_only:
            cmd.extend(["-x", "-f", "bestaudio", "--audio-format", "mp3"])
        elif extra_args:
            cmd.extend(extra_args)

        # Add browser args
        cmd.extend(self._get_browser_args())

        try:
            subprocess.run(cmd, check=True, shell=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Download failed: {e}")
            return False

    def get_thumbnail(self, url: str) -> Optional[str]:
        """Get thumbnail URL for video"""
        data = self.fetch_json(url, flat=False)
        if not data:
            return None

        try:
            thumbnails = data.get("thumbnails", [])
            if thumbnails:
                return thumbnails[-1].get("url")
        except (KeyError, IndexError):
            pass

        return None

    def search(
        self,
        query: str,
        filters: Optional[str] = None,
        max_results: Optional[int] = None
    ) -> Optional[List[Dict]]:
        """
        Search YouTube

        Args:
            query: Search query
            filters: YouTube search filters (sp parameter)
            max_results: Maximum number of results

        Returns:
            List of video entries
        """
        # Encode query for URL
        import urllib.parse
        encoded_query = urllib.parse.quote(query)

        url = f"https://www.youtube.com/results?search_query={encoded_query}"
        if filters:
            url += f"&sp={filters}"

        data = self.fetch_json(url, flat=True)

        if not data:
            return None

        entries = data.get("entries", [])

        if max_results:
            entries = entries[:max_results]

        return entries

    def get_channel_videos(self, channel_url: str) -> Optional[List[Dict]]:
        """Get videos from a channel"""
        return self.search(channel_url)

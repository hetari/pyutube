import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

from pyutube.services.models import PlaylistDownloadPlan
from pyutube.services.YtDlpService import YtDlpService
from pyutube.utils import (
    ask_for_make_playlist_in_order,
    ask_playlist_download_mode,
    ask_playlist_video_names,
    asking_video_or_audio,
    console,
    safe_filename,
)


class PlaylistHandler:
    def __init__(self, url: str, path: str, ytdlp_args: Optional[list[str]] = None):
        self.url = url
        self.path = path
        self.playlist_videos: list = []
        self.ytdlp_args = list(ytdlp_args or [])

    def process_playlist(self) -> Optional[PlaylistDownloadPlan]:
        """Collect playlist metadata and ask the user what to download."""
        console.print("Processing playlist...")

        console.print("Loading playlist items...", style="info")
        playlist = YtDlpService(self.url, "", self.ytdlp_args).extract_info(
            noplaylist=False,
            extract_flat=True,
        )
        playlist_title = safe_filename(playlist.get("title") or "playlist")
        playlist_videos = playlist.get("entries") or []
        playlist_total = playlist.get("playlist_count") or len(playlist_videos)

        make_in_order = ask_for_make_playlist_in_order()
        if make_in_order is None:
            console.print("Cancelled")
            return None

        console.print(
            f"{'✅' if make_in_order else '❌'} Make playlist in order",
            style="info",
        )
        console.print()
        console.print("Fetching playlist videos...", style="info")
        self.get_all_playlist_videos_title(playlist_videos)

        if make_in_order:
            self.playlist_videos = [
                (f"{index + 1}__{title}", video_id)
                for index, (title, video_id) in enumerate(self.playlist_videos)
            ]

        console.print("Checking if the videos are already downloaded...")
        new_path = self.check_for_downloaded_videos(playlist_title, playlist_total)

        download_mode = ask_playlist_download_mode()
        if download_mode is None:
            console.print("Cancelled")
            return None
        if download_mode == "Download all":
            videos_selected = [video_id for _title, video_id in self.playlist_videos]
        else:
            console.print("Choose which videos you want to download", style="info")
            videos_selected = ask_playlist_video_names(self.playlist_videos)
            if videos_selected is None:
                console.print("Cancelled")
                return None

        is_audio = asking_video_or_audio()
        if is_audio is None:
            console.print("Cancelled")
            return None

        return PlaylistDownloadPlan(
            new_path=new_path,
            is_audio=is_audio,
            videos_selected=videos_selected,
            make_in_order=make_in_order,
            playlist_videos=self.playlist_videos,
        )

    def get_all_playlist_videos_title(self, videos):
        """Fetch playlist titles while preserving their original order."""
        with ThreadPoolExecutor() as executor:
            self.playlist_videos = [
                item for item in executor.map(self._extract_video_data, videos) if item[1]
            ]

    @staticmethod
    def _extract_video_data(video):
        if video is None:
            return "download", ""

        return (
            safe_filename(video.get("title") or video.get("id") or "download"),
            video.get("id") or "",
        )

    @staticmethod
    def show_playlist_info(title, total):
        console.print(f"\nPlaylist title: {title}\n", style="info")
        console.print(f"Total videos: {total}\n", style="info")

    def create_playlist_folder(self, title):
        os.makedirs(title, exist_ok=True)
        return os.path.join(self.path, title)

    def check_for_downloaded_videos(self, title, total):
        new_path = self.create_playlist_folder(safe_filename(title))
        existing_titles = {
            self._clean_downloaded_title(file_name)
            for file_name in os.listdir(new_path)
        }

        self.playlist_videos = [
            video
            for video in self.playlist_videos
            if not any(video[0].startswith(existing) for existing in existing_titles)
        ]

        if not self.playlist_videos:
            console.print(
                f"All playlist videos are already downloaded in this directory, see '{title}' folder",
                style="info",
            )
            sys.exit()

        self.show_playlist_info(title, total)
        return new_path

    @staticmethod
    def _clean_downloaded_title(file_name):
        base_name = os.path.splitext(file_name)[0]
        return re.compile(r"(_audio|_\d{3,4}p|_\d+k|_(hd|uhd|sd))$").sub(
            "",
            base_name,
        )

import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

from pytubefix import Playlist
from pytubefix.helpers import safe_filename

from pyutube.services.models import PlaylistDownloadPlan
from pyutube.utils import (
    ask_for_make_playlist_in_order,
    ask_playlist_video_names,
    asking_video_or_audio,
    console,
)


class PlaylistHandler:
    def __init__(self, url: str, path: str):
        self.url = url
        self.path = path
        self.playlist_videos: list = []

    def process_playlist(self) -> Optional[PlaylistDownloadPlan]:
        """Collect playlist metadata and ask the user what to download."""
        console.print("Processing playlist...")

        is_audio = asking_video_or_audio()
        if is_audio is None:
            console.print("Cancelled")
            return None

        console.print("Downloading playlist...")
        playlist = Playlist(self.url)

        playlist_title = playlist.title
        playlist_total = playlist.length
        playlist_videos = playlist.videos

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

        console.print("Choose which videos you want to download", style="info")
        videos_selected = ask_playlist_video_names(self.playlist_videos)
        if videos_selected is None:
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
            self.playlist_videos = list(executor.map(self._extract_video_data, videos))

    @staticmethod
    def _extract_video_data(video):
        return safe_filename(video.title), video.video_id

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
        return re.compile(r"(_\d{3,4}p|_\d+k|_(hd|uhd|sd))$").sub("", base_name)

"""Download a single YouTube video or audio stream."""

import os
import sys
from typing import Any, Optional

from pytubefix.helpers import safe_filename

from pyutube.services.FileConflictResolver import FileConflictResolver
from pyutube.services.FileService import FileService
from pyutube.services.models import DownloadPreparation
from pyutube.services.VideoService import VideoService
from pyutube.ui import console, error_console


class SingleDownloadService:
    """Coordinate the full download flow for one video."""

    def __init__(
        self,
        url: str,
        path: str,
        quality: str,
        is_audio: bool = False,
        make_playlist_in_order: bool = False,
        video_service: Optional[Any] = None,
        file_service: Optional[Any] = None,
        conflict_resolver: Optional[Any] = None,
    ) -> None:
        self.url = url
        self.path = path
        self.quality = quality
        self.is_audio = is_audio
        self.make_playlist_in_order = make_playlist_in_order
        self.file_service = file_service or FileService()
        self.conflict_resolver = conflict_resolver or FileConflictResolver(
            self.file_service
        )
        self.video_service = video_service or VideoService(self.url, self.quality, self.path)

    def refresh_video_service(self) -> None:
        """Rebuild the video service when the target URL or path changes."""
        self.video_service = VideoService(self.url, self.quality, self.path)

    def prepare_download(self) -> DownloadPreparation:
        """Resolve the current YouTube object and its downloadable streams."""
        preparation = self.video_service.get_selected_stream(
            self.video_service.search_process(),
            self.is_audio,
        )
        console.print(f"Title: {preparation.video.title}\n", style="info")
        self.quality = preparation.quality
        return preparation

    def download(self, title_number: int = 0):
        """Download either audio only or the merged video package."""
        preparation = self.prepare_download()
        video = preparation.video
        streams = preparation.streams
        video_audio = preparation.video_audio
        self.quality = preparation.quality

        if self.is_audio:
            self.download_audio(video, video_audio, title_number)
            return True

        video_file = self.video_service.get_video_streams(self.quality, streams)
        if not video_file:
            error_console.print("Something went wrong while downloading the video.")
            sys.exit()

        return self.download_video(video, video_file, video_audio, title_number)

    def download_audio(
        self,
        video: Any,
        video_audio: Any,
        title_number: int = 0,
    ) -> str:
        """Download the audio stream for a video."""
        audio_filename = self.file_service.generate_filename(
            video_audio,
            is_audio=True,
        )

        if self.make_playlist_in_order:
            base_name, extension = os.path.splitext(audio_filename)
            audio_filename = f"{title_number}__{base_name}{extension}"

        audio_filename = self.conflict_resolver.resolve(
            video,
            audio_filename,
            self.path,
            True,
        )

        try:
            if self.is_audio:
                console.print("⏳ Downloading the audio...", style="info")

            self.file_service.save_file(video_audio, audio_filename, self.path)
        except Exception as error:
            error_console.print(
                f"❗ Error (please report this in github issue: https://github.com/Hetari/pyutube/issues):\n {error}"
            )
            sys.exit()

        if self.is_audio:
            console.print("\n\n✅ Download completed", style="success")

        return audio_filename

    def download_video(
        self,
        video: Any,
        video_stream: Any,
        video_audio: Any,
        title_number: int = 0,
    ):
        """Download and merge the video and audio streams."""
        video_filename = self.file_service.generate_filename(video_stream)

        if self.make_playlist_in_order:
            video_base_name, video_extension = os.path.splitext(video_filename)
            video_filename = f"{title_number}__{video_base_name}{video_extension}"

        video_filename = self.conflict_resolver.resolve(
            video,
            video_filename,
            self.path,
            self.is_audio,
        )

        try:
            console.print("⏳ Downloading the video...", style="info")
            self.file_service.save_file(video_stream, video_filename, self.path)
            audio_filename = self.download_audio(
                video,
                video_audio,
                title_number,
            )

            video_base_name, video_extension = os.path.splitext(video_filename)
            audio_base_name, audio_extension = os.path.splitext(audio_filename)
            video_safe_filename = f"{safe_filename(video_base_name)}{video_extension}"
            audio_safe_filename = f"{safe_filename(audio_base_name)}{audio_extension}"

            self.video_service.merging(video_safe_filename, audio_safe_filename)
        except Exception as error:
            error_console.print(
                f"❗ Error (please report this in github issue: https://github.com/Hetari/pyutube/issues):\n {error}"
            )
            sys.exit()

        console.print("\n\n✅ Download completed", style="success")
        return self.quality

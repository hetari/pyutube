"""Download a single YouTube video or audio stream."""

import os
import sys
from typing import Any, Optional

from pyutube.services.FileConflictResolver import FileConflictResolver
from pyutube.services.FileService import FileService
from pyutube.services.models import DownloadPreparation
from pyutube.services.VideoService import VideoService
from pyutube.services.YtDlpService import YtDlpService
from pyutube.ui import console, error_console
from pyutube.utils import handle_error, logger


class SingleDownloadService:
    """Coordinate the full download flow for one video."""

    def __init__(
        self,
        url: str,
        path: str,
        quality: str,
        is_audio: bool = False,
        make_playlist_in_order: bool = False,
        ytdlp_args: Optional[list[str]] = None,
        video_service: Optional[Any] = None,
        file_service: Optional[Any] = None,
        conflict_resolver: Optional[Any] = None,
        audio_converter: Optional[Any] = None,
    ) -> None:
        self.url = url
        self.path = path
        self.quality = quality
        self.is_audio = is_audio
        self.audio_format = "mp3"
        self.make_playlist_in_order = make_playlist_in_order
        self.ytdlp_args = list(ytdlp_args or [])
        self.file_service = file_service or FileService()
        self.conflict_resolver = conflict_resolver or FileConflictResolver(
            self.file_service
        )
        self.video_service = video_service or VideoService(
            self.url, self.quality, self.path, self.ytdlp_args
        )
        self.backend = YtDlpService(self.url, self.path, self.ytdlp_args)
        self.audio_converter = audio_converter

    def refresh_video_service(self) -> None:
        """Rebuild the video service when the target URL or path changes."""
        self.video_service = VideoService(
            self.url,
            self.quality,
            self.path,
            self.ytdlp_args,
        )
        self.backend = YtDlpService(self.url, self.path, self.ytdlp_args)

    def prepare_download(self) -> DownloadPreparation:
        """Resolve the current video metadata and its downloadable formats."""
        logger.log(
            "SingleDownloadService.prepare_download",
            {"url": self.url, "quality": self.quality, "is_audio": self.is_audio},
        )
        preparation = self.video_service.get_selected_stream(
            self.video_service.search_process(),
            self.is_audio,
        )
        console.print(
            f"Title: {preparation.video.get('title', 'Unknown')}\n",
            style="info",
        )
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

        return self.download_video(video, video_file, title_number)

    def download_audio(
        self,
        video: Any,
        video_audio: Any,
        title_number: int = 0,
    ) -> str:
        """Download the audio stream for a video."""
        video_title = video.get("title") or video.get("fulltitle") or video.get("id")
        audio_filename = self.file_service.generate_filename(
            video_audio,
            is_audio=True,
            title=video_title or "",
        )

        if self.make_playlist_in_order:
            base_name, extension = os.path.splitext(audio_filename)
            audio_filename = f"{title_number}__{base_name}{extension}"

        resolved_audio_filename = self.conflict_resolver.resolve(
            video,
            audio_filename,
            self.path,
            True,
        )
        if resolved_audio_filename is None:
            if self.is_audio:
                console.print("\n\n✅ Download completed", style="success")
            return audio_filename

        audio_filename = resolved_audio_filename

        logger.log(
            "SingleDownloadService.download_audio",
            {
                "audio_filename": audio_filename,
                "audio_format": self.audio_format,
                "path": self.path,
            },
        )
        try:
            console.print("⏳ Downloading the audio...", style="info")
            self.backend.download_audio(audio_filename, self.audio_format)
        except Exception as error:
            handle_error(error, context="Downloading audio")
            sys.exit(1)

        if self.is_audio:
            console.print("\n\n✅ Download completed", style="success")

        return audio_filename

    def download_video(
        self,
        video: Any,
        video_stream: Any,
        title_number: int = 0,
    ):
        """Download the selected video format and let yt-dlp merge audio."""
        video_title = video.get("title") or video.get("fulltitle") or video.get("id")
        video_filename = self.file_service.generate_filename(
            video_stream,
            title=video_title or "",
        )

        if self.make_playlist_in_order:
            video_base_name, video_extension = os.path.splitext(video_filename)
            video_filename = f"{title_number}__{video_base_name}{video_extension}"

        resolved_video_filename = self.conflict_resolver.resolve(
            video,
            video_filename,
            self.path,
            self.is_audio,
        )
        if resolved_video_filename is None:
            console.print("Using existing video file", style="info")
            console.print("\n\n✅ Download completed", style="success")
            return self.quality

        video_filename = resolved_video_filename

        logger.log(
            "SingleDownloadService.download_video",
            {
                "video_filename": video_filename,
                "format_id": video_stream.get("format_id"),
                "path": self.path,
            },
        )
        try:
            console.print("⏳ Downloading the video...", style="info")
            self.backend.download_video(video_filename, video_stream["format_id"])
        except Exception as error:
            handle_error(error, context="Downloading video")
            sys.exit(1)

        console.print("\n\n✅ Download completed", style="success")
        return self.quality

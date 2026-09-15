"""Download a single YouTube video or audio stream."""

import os
from typing import Any, Optional, Sequence

from pyutube.core.exceptions import NoStreamAvailableError
from pyutube.core.logger import logger
from pyutube.services.FileConflictResolver import FileConflictResolver
from pyutube.services.FileService import FileService
from pyutube.services.models import DownloadPreparation, FormatInfo, VideoInfo
from pyutube.services.StreamSelectionService import StreamSelectionService
from pyutube.services.VideoSearchService import VideoSearchService
from pyutube.services.YtDlpService import YtDlpService
from pyutube.ui import console


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
        search_service: Optional[VideoSearchService] = None,
        stream_selection_service: Optional[StreamSelectionService] = None,
        file_service: Optional[FileService] = None,
        conflict_resolver: Optional[FileConflictResolver] = None,
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
        self.search_service = search_service or VideoSearchService(
            self.url, self.ytdlp_args
        )
        self.stream_selection_service = stream_selection_service or StreamSelectionService(
            self.quality
        )
        self.backend = YtDlpService(self.url, self.path, self.ytdlp_args)
        self.audio_converter = audio_converter

    def refresh_services(self) -> None:
        """Rebuild child services when the target URL, quality, or path changes."""
        self.search_service = VideoSearchService(self.url, self.ytdlp_args)
        self.stream_selection_service = StreamSelectionService(self.quality)
        self.backend = YtDlpService(self.url, self.path, self.ytdlp_args)

    def refresh_video_service(self) -> None:
        """Compatibility alias for refresh_services."""
        self.refresh_services()

    @property
    def video_service(self) -> Any:
        """Compatibility accessor returning self for historic facade methods."""
        return self

    def get_video_streams(self, quality: str, streams: Sequence[FormatInfo]) -> FormatInfo:
        """Compatibility delegate to stream_selection_service."""
        return self.stream_selection_service.get_video_streams(quality, streams)

    def prepare_download(self) -> DownloadPreparation:
        """Resolve the current video metadata and its downloadable formats."""
        logger.log(
            "SingleDownloadService.prepare_download",
            {"url": self.url, "quality": self.quality, "is_audio": self.is_audio},
        )
        video_metadata = self.search_service.search_process()
        preparation = self.stream_selection_service.get_selected_stream(
            video_metadata,
            self.is_audio,
        )
        console.print(
            f"Title: {preparation.video.get('title', 'Unknown')}\n",
            style="info",
        )
        self.quality = preparation.quality
        return preparation

    def download(self, title_number: int = 0) -> Any:
        """Download either audio only or the merged video package."""
        preparation = self.prepare_download()
        video = preparation.video
        streams = preparation.streams
        video_audio = preparation.video_audio
        self.quality = preparation.quality

        if self.is_audio:
            self.download_audio(video, video_audio, title_number)
            return True

        video_file = self.stream_selection_service.get_video_streams(self.quality, streams)
        if not video_file:
            raise NoStreamAvailableError("Something went wrong while downloading the video.")

        return self.download_video(video, video_file, title_number)

    def download_audio(
        self,
        video: VideoInfo,
        video_audio: Optional[FormatInfo],
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
        console.print("⏳ Downloading the audio...", style="info")
        self.backend.download_audio(audio_filename, self.audio_format)

        if self.is_audio:
            console.print("\n\n✅ Download completed", style="success")

        return audio_filename

    def download_video(
        self,
        video: VideoInfo,
        video_stream: FormatInfo,
        title_number: int = 0,
    ) -> str:
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
        console.print("⏳ Downloading the video...", style="info")
        self.backend.download_video(video_filename, str(video_stream.get("format_id") or ""))

        console.print("\n\n✅ Download completed", style="success")
        return self.quality

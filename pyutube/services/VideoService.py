"""Compatibility façade for the split video services."""

from typing import Optional, Sequence

from pyutube.services.models import (
    AvailableVideoStreams,
    DownloadPreparation,
    FormatInfo,
    VideoInfo,
)
from pyutube.services.StreamSelectionService import StreamSelectionService
from pyutube.services.VideoSearchService import VideoSearchService


class VideoService:
    """Keep the historic service API while delegating to focused classes."""

    def __init__(
        self,
        url: str,
        quality: str,
        path: str = "",
        ytdlp_args: Optional[list[str]] = None,
    ) -> None:
        self.url = url
        self.quality = quality
        self.path = path
        self.ytdlp_args = list(ytdlp_args or [])
        self.search_service = VideoSearchService(url, self.ytdlp_args)
        self.stream_selection_service = StreamSelectionService(quality)

    def _sync(self) -> None:
        self.search_service.url = self.url
        self.search_service.ytdlp_args = list(self.ytdlp_args)
        self.stream_selection_service.quality = self.quality

    def search_process(self) -> VideoInfo:
        self._sync()
        return self.search_service.search_process()

    def get_available_resolutions(self, video: VideoInfo) -> AvailableVideoStreams:
        self._sync()
        return self.stream_selection_service.get_available_resolutions(video)

    def get_video_streams(self, quality: str, streams: Sequence[FormatInfo]) -> FormatInfo:
        self._sync()
        return self.stream_selection_service.get_video_streams(quality, streams)

    def get_selected_stream(self, video: VideoInfo, is_audio: bool = False) -> DownloadPreparation:
        self._sync()
        preparation = self.stream_selection_service.get_selected_stream(
            video,
            is_audio,
        )
        self.quality = self.stream_selection_service.quality
        return preparation

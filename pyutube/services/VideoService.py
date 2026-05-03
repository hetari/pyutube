"""Compatibility façade for the split video services."""

from pyutube.services.StreamSelectionService import StreamSelectionService
from pyutube.services.VideoMergeService import VideoMergeService
from pyutube.services.VideoSearchService import VideoSearchService


class VideoService:
    """Keep the historic service API while delegating to focused classes."""

    def __init__(self, url: str, quality: str, path: str) -> None:
        self.url = url
        self.quality = quality
        self.path = path
        self.search_service = VideoSearchService(url)
        self.stream_selection_service = StreamSelectionService(quality)
        self.merge_service = VideoMergeService(path)

    def _sync(self) -> None:
        self.search_service.url = self.url
        self.stream_selection_service.quality = self.quality
        self.merge_service.path = self.path

    def search_process(self):
        self._sync()
        return self.search_service.search_process()

    def get_available_resolutions(self, video):
        self._sync()
        return self.stream_selection_service.get_available_resolutions(video)

    def get_video_streams(self, quality: str, streams):
        self._sync()
        return self.stream_selection_service.get_video_streams(quality, streams)

    def get_selected_stream(self, video, is_audio: bool = False):
        self._sync()
        preparation = self.stream_selection_service.get_selected_stream(
            video,
            is_audio,
        )
        self.quality = self.stream_selection_service.quality
        return preparation

    def merging(self, video_name: str, audio_name: str):
        self._sync()
        return self.merge_service.merging(video_name, audio_name)

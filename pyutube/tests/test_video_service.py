from types import SimpleNamespace
from unittest.mock import Mock

from pyutube.services.VideoService import VideoService


def test_video_service_facade_delegates():
    service = VideoService("https://example.com", "720p", "/tmp")
    service.search_service = Mock()
    service.stream_selection_service = Mock()
    service.merge_service = Mock()

    service.search_service.search_process.return_value = "video"
    service.stream_selection_service.get_available_resolutions.return_value = "resolutions"
    service.stream_selection_service.get_video_streams.return_value = "stream"
    service.stream_selection_service.get_selected_stream.return_value = SimpleNamespace(quality="1080p")
    service.merge_service.merging.return_value = "merged"

    assert service.search_process() == "video"
    assert service.get_available_resolutions("video") == "resolutions"
    assert service.get_video_streams("720p", "streams") == "stream"
    assert service.get_selected_stream("video").quality == "1080p"
    assert service.merging("video", "audio") == "merged"

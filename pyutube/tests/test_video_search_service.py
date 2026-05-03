from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from pyutube.services.VideoSearchService import VideoSearchService


def test_video_search_service_branches(monkeypatch):
    service = VideoSearchService("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    video = SimpleNamespace(title="Demo")
    youtube_mock = Mock(return_value=video)
    monkeypatch.setattr("pyutube.services.VideoSearchService.YouTube", youtube_mock)
    monkeypatch.setattr("pyutube.services.VideoSearchService.error_console.print", Mock())
    assert service.search_process() is video
    youtube_mock.assert_called_once()
    assert youtube_mock.call_args.kwargs["client"] == "ANDROID_VR"
    assert youtube_mock.call_args.kwargs["use_oauth"] is False

    monkeypatch.setattr("pyutube.services.VideoSearchService.YouTube", lambda *args, **kwargs: None)
    with pytest.raises(SystemExit):
        service.search_process()

    monkeypatch.setattr(
        "pyutube.services.VideoSearchService.VideoSearchService._video_search",
        lambda self: (_ for _ in ()).throw(RuntimeError("boom")),
    )
    with pytest.raises(SystemExit):
        service.search_process()

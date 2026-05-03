from types import SimpleNamespace

import pytest

from pyutube.services.models import DownloadPreparation
from pyutube.services.StreamSelectionService import StreamSelectionService


class FakeAudioQuery:
    def __init__(self, stream):
        self.stream = stream

    def order_by(self, _field):
        return self

    def first(self):
        return self.stream


class FakeStreamCollection(list):
    def __init__(self, video_streams, audio_stream):
        super().__init__(video_streams)
        self.audio_stream = audio_stream

    def filter(self, progressive=False, adaptive=True, mime_type=None, only_audio=False, res=None):
        if only_audio:
            return FakeAudioQuery(self.audio_stream)

        if res is not None:
            matches = [stream for stream in self if stream.resolution == res]
            return FakeStreamCollection(matches, self.audio_stream)

        return self

    def first(self):
        return self[0] if self else None


class FakeStream:
    def __init__(self, resolution, filesize, is_progressive=True, mime_type="video/mp4"):
        self.resolution = resolution
        self.filesize = filesize
        self.is_progressive = is_progressive
        self.mime_type = mime_type


class FakeVideo:
    def __init__(self, streams, title="Demo"):
        self.streams = streams
        self.title = title


def test_stream_selection_service_branches(monkeypatch):
    video_streams = FakeStreamCollection(
        [
            FakeStream("360p", 2 * 1024 * 1024),
            FakeStream("720p", 4 * 1024 * 1024, is_progressive=False),
        ],
        SimpleNamespace(filesize=1024 * 1024),
    )
    video = FakeVideo(video_streams)
    service = StreamSelectionService("")

    monkeypatch.setattr("pyutube.services.StreamSelectionService.ask_resolution", lambda resolutions, sizes: "720p")
    available = service.get_available_resolutions(video)
    assert available.resolutions == ["360p", "720p"]
    assert available.sizes[0].endswith("MB")

    service.quality = "720p"
    preparation = service.get_selected_stream(video, is_audio=False)
    assert preparation.quality == "720p"

    service.quality = "Cancel"
    with pytest.raises(SystemExit):
        service.get_video_streams("Cancel", video_streams)

    assert service.get_video_streams("720p", video_streams).resolution == "720p"

    no_match_streams = FakeStreamCollection([FakeStream("360p", 1)], SimpleNamespace(filesize=1))
    assert service.get_video_streams("480p", no_match_streams).resolution == "360p"


def test_stream_selection_service_returns_download_preparation(monkeypatch):
    video_streams = FakeStreamCollection(
        [
            FakeStream("360p", 2 * 1024 * 1024),
            FakeStream("720p", 4 * 1024 * 1024, is_progressive=False),
        ],
        SimpleNamespace(filesize=1024 * 1024),
    )
    video = FakeVideo(video_streams)
    service = StreamSelectionService("")

    monkeypatch.setattr(
        "pyutube.services.StreamSelectionService.ask_resolution",
        lambda resolutions, sizes: "720p",
    )

    preparation = service.get_selected_stream(video, is_audio=False)

    assert isinstance(preparation, DownloadPreparation)
    assert preparation.video is video
    assert preparation.quality == "720p"
    assert list(preparation.streams) == list(video_streams)
    assert preparation.video_audio.filesize == 1024 * 1024


def test_stream_selection_service_skips_prompt_when_audio(monkeypatch):
    video_streams = FakeStreamCollection(
        [FakeStream("360p", 2 * 1024 * 1024)],
        SimpleNamespace(filesize=1024 * 1024),
    )
    video = FakeVideo(video_streams)
    service = StreamSelectionService("1080p")

    def fail_if_called(*args, **kwargs):
        raise AssertionError("ask_resolution should not be called for audio-only downloads")

    monkeypatch.setattr("pyutube.services.StreamSelectionService.ask_resolution", fail_if_called)

    preparation = service.get_selected_stream(video, is_audio=True)

    assert preparation.quality == "1080p"
    assert preparation.video_audio.filesize == 1024 * 1024

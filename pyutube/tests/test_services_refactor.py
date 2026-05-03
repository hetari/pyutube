from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from pyutube.services.FileConflictResolver import FileConflictResolver
from pyutube.services.models import DownloadPreparation, PlaylistDownloadPlan
from pyutube.services.PlaylistDownloadService import PlaylistDownloadService
from pyutube.services.SingleDownloadService import SingleDownloadService
from pyutube.services.StreamSelectionService import StreamSelectionService
from pyutube.services.VideoMergeService import VideoMergeService


class FakeStream:
    def __init__(self, resolution, filesize, is_progressive=True):
        self.resolution = resolution
        self.filesize = filesize
        self.is_progressive = is_progressive


class FakeAudioQuery:
    def __init__(self, audio_stream):
        self.audio_stream = audio_stream

    def order_by(self, _field):
        return self

    def first(self):
        return self.audio_stream


class FakeStreams(list):
    def __init__(self, video_streams, audio_stream):
        super().__init__(video_streams)
        self._audio_stream = audio_stream

    def filter(self, progressive=False, adaptive=True, mime_type=None, only_audio=False):
        if only_audio:
            return FakeAudioQuery(self._audio_stream)

        return self


class FakeVideo:
    def __init__(self, streams, title="Demo"):
        self.streams = streams
        self.title = title


def test_stream_selection_service_returns_download_preparation(monkeypatch):
    video_streams = FakeStreams(
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
    video_streams = FakeStreams(
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


def test_file_conflict_resolver_renames_existing_file(monkeypatch):
    video = object()
    file_service = Mock()
    file_service.is_file_exists.return_value = True
    file_service.generate_filename.return_value = "renamed.m4a"

    resolver = FileConflictResolver(file_service)
    monkeypatch.setattr(
        "pyutube.services.FileConflictResolver.ask_rename_file",
        lambda filename: "Rename it",
    )
    monkeypatch.setattr("builtins.input", lambda prompt: "new name")

    result = resolver.resolve(video, "old.m4a", "/tmp", True)

    assert result == "renamed.m4a"
    file_service.generate_filename.assert_called_once_with(video, True, "new name")


def test_file_conflict_resolver_cancel_exits(monkeypatch):
    file_service = Mock()
    file_service.is_file_exists.return_value = True
    resolver = FileConflictResolver(file_service)
    monkeypatch.setattr(
        "pyutube.services.FileConflictResolver.ask_rename_file",
        lambda filename: "Cancel",
    )

    with pytest.raises(SystemExit):
        resolver.resolve(object(), "old.m4a", "/tmp", True)


def test_single_download_service_prepare_download_returns_dataclass():
    video = SimpleNamespace(title="Demo Video")
    preparation = DownloadPreparation(
        video=video,
        streams="streams",
        video_audio="audio",
        quality="720p",
    )
    video_service = Mock()
    video_service.search_process.return_value = video
    video_service.get_selected_stream.return_value = preparation

    service = SingleDownloadService(
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "/tmp",
        "",
        video_service=video_service,
        file_service=Mock(),
        conflict_resolver=Mock(),
    )

    result = service.prepare_download()

    assert result is preparation
    assert service.quality == "720p"
    video_service.search_process.assert_called_once_with()
    video_service.get_selected_stream.assert_called_once_with(video, False)


def test_single_download_service_audio_conflict_uses_audio_flag():
    video = object()
    audio_stream = SimpleNamespace(
        default_filename="track.mp4",
        resolution="audio",
        mime_type="audio/mp4",
    )
    file_service = Mock()
    file_service.generate_filename.return_value = "track_audio.m4a"
    conflict_resolver = Mock()
    conflict_resolver.resolve.return_value = "track_audio.m4a"

    service = SingleDownloadService(
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "/tmp",
        "",
        is_audio=True,
        file_service=file_service,
        conflict_resolver=conflict_resolver,
    )

    service.download_audio(video, audio_stream)

    conflict_resolver.resolve.assert_called_once_with(
        video,
        "track_audio.m4a",
        "/tmp",
        True,
    )


def test_playlist_download_service_uses_playlist_plan(monkeypatch):
    plan = PlaylistDownloadPlan(
        new_path="/downloads/playlist",
        is_audio=False,
        videos_selected=["video-1", "video-2"],
        make_in_order=True,
        playlist_videos=[("1__First", "video-1"), ("2__Second", "video-2")],
    )
    handler = Mock()
    handler.process_playlist.return_value = plan
    monkeypatch.setattr(
        "pyutube.services.PlaylistDownloadService.PlaylistHandler",
        lambda url, path: handler,
    )

    created_downloaders = []

    def factory(url, path, quality, is_audio, make_playlist_in_order):
        is_first = len(created_downloaders) == 0
        downloader = Mock()
        downloader.url = url
        downloader.path = path
        downloader.quality = quality
        downloader.is_audio = is_audio
        downloader.make_playlist_in_order = make_playlist_in_order
        downloader.refresh_video_service = Mock()
        downloader.download = Mock(return_value="720p" if is_first else None)
        created_downloaders.append(downloader)
        return downloader

    service = PlaylistDownloadService(factory)
    service.download_playlist("https://www.youtube.com/playlist?list=test", "/tmp", "360p")

    assert len(created_downloaders) == 2
    assert created_downloaders[0].url.endswith("video-1")
    assert created_downloaders[1].url.endswith("video-2")
    assert created_downloaders[0].quality == "360p"
    assert created_downloaders[1].quality == "720p"
    created_downloaders[0].download.assert_called_once_with(1)
    created_downloaders[1].download.assert_called_once_with(2)


def test_video_merge_service_merging_moves_output(tmp_path, monkeypatch):
    service = VideoMergeService(str(tmp_path))
    (tmp_path / "clip_720p.mp4").write_text("video")
    (tmp_path / "clip_audio.m4a").write_text("audio")

    def fake_merge(video_path, audio_path, output_file, logger=None):
        Path(output_file).write_text("merged")

    monkeypatch.setattr(
        "pyutube.services.VideoMergeService.ffmpeg_merge_video_audio",
        fake_merge,
    )

    service.merging("clip_720p.mp4", "clip_audio.m4a")

    assert (tmp_path / "clip_720p.mp4").read_text() == "merged"
    assert not (tmp_path / "output").exists()

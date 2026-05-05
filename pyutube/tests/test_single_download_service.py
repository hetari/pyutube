from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from pyutube.services.models import DownloadPreparation
from pyutube.services.SingleDownloadService import SingleDownloadService


def test_single_download_service_refresh_video_service(monkeypatch):
    import importlib

    single_module = importlib.import_module("pyutube.services.SingleDownloadService")
    created = []

    class FakeVideoService:
        def __init__(self, url, quality, path):
            created.append((url, quality, path))

    monkeypatch.setattr(single_module, "VideoService", FakeVideoService)

    service = SingleDownloadService(
        "https://example.com",
        "/downloads",
        "720p",
        video_service=Mock(),
        file_service=Mock(),
        conflict_resolver=Mock(),
    )
    service.refresh_video_service()

    assert created == [
        ("https://example.com", "720p", "/downloads"),
    ]


def test_single_download_service_download_routes(monkeypatch):
    preparation = SimpleNamespace(
        video=SimpleNamespace(title="Demo"),
        streams="streams",
        video_audio="audio",
        quality="720p",
    )
    video_service = Mock()
    video_service.get_video_streams.return_value = "stream"
    service = SingleDownloadService(
        "https://example.com",
        "/downloads",
        "360p",
        video_service=video_service,
        file_service=Mock(),
        conflict_resolver=Mock(),
        audio_converter=Mock(),
    )
    service.prepare_download = Mock(return_value=preparation)
    service.download_audio = Mock(return_value="audio.wav")
    service.download_video = Mock(return_value="merged")

    service.is_audio = True
    assert service.download() is True
    service.download_audio.assert_called_once_with(preparation.video, preparation.video_audio, 0)
    service.download_video.assert_not_called()

    service.is_audio = False
    service.download_audio.reset_mock()
    service.download_video.reset_mock()
    assert service.download() == "merged"
    video_service.get_video_streams.assert_called_once_with("720p", "streams")
    service.download_video.assert_called_once_with(preparation.video, "stream", preparation.video_audio, 0)

    video_service.get_video_streams.return_value = None
    with pytest.raises(SystemExit):
        service.download()


def test_single_download_service_download_audio_success_and_error(monkeypatch):
    import importlib

    single_module = importlib.import_module("pyutube.services.SingleDownloadService")
    monkeypatch.setattr(single_module.console, "print", Mock())
    error_print = Mock()
    monkeypatch.setattr(single_module.error_console, "print", error_print)

    audio_stream = SimpleNamespace(
        default_filename="song.mp4",
        mime_type="audio/mp4",
        resolution="audio",
    )
    file_service = Mock()
    file_service.generate_filename.return_value = "song_audio.wav"
    file_service.save_file = Mock()
    conflict_resolver = Mock()
    conflict_resolver.resolve.return_value = "2__song_audio.wav"
    audio_converter = Mock()

    service = SingleDownloadService(
        "https://example.com",
        "/downloads",
        "720p",
        is_audio=True,
        make_playlist_in_order=True,
        file_service=file_service,
        conflict_resolver=conflict_resolver,
        audio_converter=audio_converter,
        video_service=Mock(),
    )

    result = service.download_audio("video", audio_stream, title_number=2)

    assert result == "2__song_audio.wav"
    file_service.generate_filename.assert_called_once_with(
        audio_stream,
        is_audio=True,
        audio_format="wav",
    )
    conflict_resolver.resolve.assert_called_once_with("video", "2__song_audio.wav", "/downloads", True)
    file_service.save_file.assert_called_once_with(audio_stream, "2__song_audio.m4a", "/downloads")
    audio_converter.convert_audio.assert_called_once_with(
        "/downloads/2__song_audio.m4a",
        "/downloads/2__song_audio.wav",
    )

    file_service.save_file.side_effect = RuntimeError("boom")
    with pytest.raises(SystemExit):
        service.download_audio("video", audio_stream)

    error_print.assert_called()


def test_single_download_service_download_audio_skip(monkeypatch):
    import importlib

    single_module = importlib.import_module("pyutube.services.SingleDownloadService")
    monkeypatch.setattr(single_module.console, "print", Mock())
    monkeypatch.setattr(single_module.error_console, "print", Mock())

    audio_stream = SimpleNamespace(
        default_filename="song.mp4",
        mime_type="audio/mp4",
        resolution="audio",
    )
    file_service = Mock()
    file_service.generate_filename.return_value = "song_audio.wav"
    conflict_resolver = Mock()
    conflict_resolver.resolve.return_value = None
    audio_converter = Mock()

    service = SingleDownloadService(
        "https://example.com",
        "/downloads",
        "720p",
        is_audio=True,
        file_service=file_service,
        conflict_resolver=conflict_resolver,
        audio_converter=audio_converter,
        video_service=Mock(),
    )

    result = service.download_audio("video", audio_stream)

    assert result == "song_audio.wav"
    file_service.save_file.assert_not_called()
    audio_converter.convert_audio.assert_not_called()


def test_single_download_service_download_video_skip_and_merge_existing_files(monkeypatch):
    import importlib

    single_module = importlib.import_module("pyutube.services.SingleDownloadService")
    monkeypatch.setattr(single_module, "safe_filename", lambda value: f"safe-{value}")
    monkeypatch.setattr(single_module.console, "print", Mock())
    monkeypatch.setattr(single_module.error_console, "print", Mock())

    video_stream = SimpleNamespace(
        default_filename="Regex is weird. So, I built it_144p.mp4",
        resolution="144p",
        mime_type="video/mp4",
    )
    video_audio = SimpleNamespace(
        default_filename="Regex is weird. So, I built it_audio.mp4",
        mime_type="audio/mp4",
        resolution="audio",
    )
    file_service = Mock()
    file_service.generate_filename.side_effect = [
        "Regex is weird. So, I built it_144p.mp4",
        "Regex is weird. So, I built it_audio.wav",
    ]
    conflict_resolver = Mock()
    conflict_resolver.resolve.side_effect = [None, None]
    video_service = Mock()
    video_service.merging = Mock()
    audio_converter = Mock()

    service = SingleDownloadService(
        "https://example.com",
        "/downloads",
        "144p",
        file_service=file_service,
        conflict_resolver=conflict_resolver,
        audio_converter=audio_converter,
        video_service=video_service,
    )

    result = service.download_video("video", video_stream, video_audio)

    assert result == "144p"
    file_service.save_file.assert_not_called()
    audio_converter.convert_audio.assert_not_called()
    video_service.merging.assert_called_once_with(
        "safe-Regex is weird. So, I built it_144p.mp4",
        "safe-Regex is weird. So, I built it_audio.wav",
    )


def test_single_download_service_download_video_success_and_error(monkeypatch):
    import importlib

    single_module = importlib.import_module("pyutube.services.SingleDownloadService")
    monkeypatch.setattr(single_module, "safe_filename", lambda value: f"safe-{value}")
    monkeypatch.setattr(single_module.console, "print", Mock())
    error_print = Mock()
    monkeypatch.setattr(single_module.error_console, "print", error_print)

    file_service = Mock()
    file_service.generate_filename.return_value = "clip 720p.mp4"
    file_service.save_file = Mock()
    conflict_resolver = Mock()
    conflict_resolver.resolve.return_value = "clip 720p.mp4"
    video_service = Mock()
    video_service.merging = Mock()
    audio_converter = Mock()

    service = SingleDownloadService(
        "https://example.com",
        "/downloads",
        "720p",
        file_service=file_service,
        conflict_resolver=conflict_resolver,
        audio_converter=audio_converter,
        video_service=video_service,
    )
    service.download_audio = Mock(return_value="song audio.wav")

    result = service.download_video("video", "stream", "audio", title_number=3)

    assert result == "720p"
    file_service.generate_filename.assert_called_once_with("stream")
    conflict_resolver.resolve.assert_called_once_with("video", "clip 720p.mp4", "/downloads", False)
    file_service.save_file.assert_called_once_with("stream", "clip 720p.mp4", "/downloads")
    service.download_audio.assert_called_once_with("video", "audio", 3)
    video_service.merging.assert_called_once_with("safe-clip 720p.mp4", "safe-song audio.wav")

    file_service.save_file.side_effect = RuntimeError("boom")
    with pytest.raises(SystemExit):
        service.download_video("video", "stream", "audio")

    error_print.assert_called()


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
    file_service.generate_filename.return_value = "track_audio.mp3"
    conflict_resolver = Mock()
    conflict_resolver.resolve.return_value = "track_audio.mp3"
    audio_converter = Mock()

    service = SingleDownloadService(
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "/tmp",
        "",
        is_audio=True,
        audio_format="mp3",
        file_service=file_service,
        conflict_resolver=conflict_resolver,
        audio_converter=audio_converter,
    )

    service.download_audio(video, audio_stream)

    file_service.generate_filename.assert_called_once_with(
        audio_stream,
        is_audio=True,
        audio_format="mp3",
    )
    conflict_resolver.resolve.assert_called_once_with(
        video,
        "track_audio.mp3",
        "/tmp",
        True,
    )
    file_service.save_file.assert_called_once_with(
        audio_stream,
        "track_audio.m4a",
        "/tmp",
    )
    audio_converter.convert_audio.assert_called_once_with(
        "/tmp/track_audio.m4a",
        "/tmp/track_audio.mp3",
    )

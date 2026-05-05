from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from pyutube import cli


def test_cli_branches(monkeypatch):
    class FakeURLHandler:
        def __init__(self, url):
            self.url = url

        def validate(self):
            return True, "video"

    class FakeVideoService:
        def get_video_streams(self, quality, streams):
            return "stream"

    class FakeDownloadService:
        def __init__(self, *args, **kwargs):
            self.is_audio = False
            self.video_service = FakeVideoService()
            self.download_preparing_result = SimpleNamespace(
                video=SimpleNamespace(title="Demo"),
                streams="streams",
                video_audio="audio",
                quality="720p",
            )
            self.download_preparing = Mock(return_value=self.download_preparing_result)
            self.download_audio = Mock()
            self.download_video = Mock()
            self.asking_video_or_audio = Mock()
            self.get_playlist_links = Mock()

    fake = FakeDownloadService()
    captured_kwargs = {}
    monkeypatch.setattr("pyutube.cli.check_for_updates", lambda: None)
    monkeypatch.setattr("pyutube.cli.clear", lambda: None)
    monkeypatch.setattr("pyutube.cli.check_internet_connection", lambda: True)
    monkeypatch.setattr("pyutube.cli.URLHandler", FakeURLHandler)
    monkeypatch.setattr(
        "pyutube.cli.DownloadService",
        lambda *args, **kwargs: captured_kwargs.update(kwargs) or fake,
    )
    monkeypatch.setattr("pyutube.cli.sys.exit", Mock(side_effect=SystemExit))

    with pytest.raises(SystemExit):
        cli.pyutube(
            url="https://example.com/watch?v=1",
            path="/tmp",
            audio=True,
            mp3=True,
            video=False,
            version=False,
    )
    fake.download_preparing.assert_called_once()
    fake.download_audio.assert_called_once()
    assert captured_kwargs["audio_format"] == "mp3"

    fake.download_preparing.reset_mock()
    fake.download_audio.reset_mock()
    fake.download_video.reset_mock()
    fake.asking_video_or_audio.reset_mock()
    fake.get_playlist_links.reset_mock()

    monkeypatch.setattr("pyutube.cli.URLHandler", lambda url: SimpleNamespace(validate=lambda: (True, "short")))
    with pytest.raises(SystemExit):
        cli.pyutube(
            url="https://example.com/watch?v=1",
            path="/tmp",
            audio=False,
            video=True,
            version=False,
        )
    fake.download_preparing.assert_called_once()
    fake.download_video.assert_called_once()

    fake.download_preparing.reset_mock()
    fake.download_video.reset_mock()
    monkeypatch.setattr("pyutube.cli.URLHandler", lambda url: SimpleNamespace(validate=lambda: (True, "video")))
    with pytest.raises(SystemExit):
        cli.pyutube(
            url="https://example.com/watch?v=1",
            path="/tmp",
            audio=False,
            video=False,
            version=False,
        )
    fake.asking_video_or_audio.assert_called_once()

    fake.asking_video_or_audio.reset_mock()
    monkeypatch.setattr("pyutube.cli.URLHandler", lambda url: SimpleNamespace(validate=lambda: (True, "playlist")))
    with pytest.raises(SystemExit):
        cli.pyutube(
            url="https://example.com/playlist?list=1",
            path="/tmp",
            audio=False,
            video=False,
            version=False,
        )
    fake.get_playlist_links.assert_called_once()


def test_cli_version_skips_update_check(monkeypatch):
    check_updates = Mock()
    print_mock = Mock()
    monkeypatch.setattr("pyutube.cli.check_for_updates", check_updates)
    monkeypatch.setattr("pyutube.cli.console.print", print_mock)
    monkeypatch.setattr("pyutube.cli.sys.exit", Mock(side_effect=SystemExit))

    with pytest.raises(SystemExit):
        cli.pyutube(version=True, audio=False, video=False)

    check_updates.assert_not_called()
    print_mock.assert_called_once()

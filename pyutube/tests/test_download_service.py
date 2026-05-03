from types import SimpleNamespace
from unittest.mock import Mock

from pyutube.services.DownloadService import DownloadService
from pyutube.services.models import DownloadPreparation


def test_download_service_delegates_to_worker(monkeypatch):
    preparation = DownloadPreparation(
        video=SimpleNamespace(title="Demo"),
        streams="streams",
        video_audio="audio",
        quality="720p",
    )
    worker = Mock()
    worker.video_service = Mock()
    worker.file_service = Mock()
    worker.refresh_video_service = Mock()
    worker.prepare_download.return_value = preparation
    worker.download.return_value = True
    worker.download_audio.return_value = "audio.mp3"
    worker.download_video.return_value = "720p"
    playlist_service = Mock()

    monkeypatch.setattr(
        "pyutube.services.DownloadService.SingleDownloadService",
        lambda **kwargs: worker,
    )
    monkeypatch.setattr(
        "pyutube.services.DownloadService.PlaylistDownloadService",
        lambda factory: playlist_service,
    )

    service = DownloadService("https://example.com", "/tmp", "360p")
    service.single_download_service = worker
    service.playlist_download_service = playlist_service
    service.download_preparing()
    service.download_audio(preparation.video, preparation.video_audio)
    service.download_video(preparation.video, "video", preparation.video_audio)
    service.get_playlist_links()

    worker.prepare_download.assert_called_once()
    worker.download_audio.assert_called_once()
    worker.download_video.assert_called_once()
    playlist_service.download_playlist.assert_called_once_with(
        "https://example.com",
        "/tmp",
        "720p",
    )


def test_download_service_question_branch(monkeypatch):
    worker = Mock()
    worker.video_service = Mock()
    worker.file_service = Mock()
    worker.refresh_video_service = Mock()
    worker.download = Mock()
    monkeypatch.setattr(
        "pyutube.services.DownloadService.SingleDownloadService",
        lambda **kwargs: worker,
    )
    monkeypatch.setattr(
        "pyutube.services.DownloadService.PlaylistDownloadService",
        lambda factory: Mock(),
    )
    monkeypatch.setattr("pyutube.services.DownloadService.asking_video_or_audio", lambda: True)

    service = DownloadService("https://example.com", "/tmp", "")
    service.single_download_service = worker
    service.is_audio = False
    service.asking_video_or_audio()

    assert service.is_audio is True
    worker.download.assert_called_once()

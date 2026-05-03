from unittest.mock import Mock

from pyutube.services.models import PlaylistDownloadPlan
from pyutube.services.PlaylistDownloadService import PlaylistDownloadService


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

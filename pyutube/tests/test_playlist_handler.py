from pathlib import Path
from types import SimpleNamespace

from pyutube.handlers.PlaylistHandler import PlaylistHandler


def test_playlist_handler_process_playlist(monkeypatch, tmp_path):
    import importlib

    playlist_module = importlib.import_module("pyutube.handlers.PlaylistHandler")

    class FakePlaylist:
        def __init__(self, url):
            self.title = "My Playlist"
            self.length = 2
            self.videos = [
                SimpleNamespace(title="Video One", video_id="id1"),
                SimpleNamespace(title="Video Two", video_id="id2"),
            ]

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(playlist_module, "Playlist", FakePlaylist)
    monkeypatch.setattr(playlist_module, "asking_video_or_audio", lambda: False)
    monkeypatch.setattr(
        playlist_module,
        "ask_for_make_playlist_in_order",
        lambda: True,
    )
    monkeypatch.setattr(
        playlist_module,
        "ask_playlist_video_names",
        lambda videos: [videos[0][1]],
    )

    handler = PlaylistHandler("https://example.com/playlist", str(tmp_path))
    plan = handler.process_playlist()

    assert plan is not None
    assert Path(plan.new_path) == tmp_path / "My Playlist"
    assert plan.is_audio is False
    assert plan.make_in_order is True
    assert plan.videos_selected == ["id1"]
    assert plan.playlist_videos[0][0].startswith("1__")


def test_playlist_handler_cancel(monkeypatch):
    import importlib

    playlist_module = importlib.import_module("pyutube.handlers.PlaylistHandler")

    monkeypatch.setattr(playlist_module, "asking_video_or_audio", lambda: None)
    handler = PlaylistHandler("https://example.com/playlist", "/tmp")

    assert handler.process_playlist() is None

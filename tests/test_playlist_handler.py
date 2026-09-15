"""Unit tests for PlaylistHandler."""

import os

import pytest

from pyutube.core.exceptions import DownloadCancelledError
from pyutube.handlers.PlaylistHandler import PlaylistHandler


class TestPlaylistHandler:
    def test_create_playlist_folder_relative_to_path(self, tmp_path):
        target_dir = tmp_path / "custom_download_dir"
        target_dir.mkdir()

        handler = PlaylistHandler(url="https://youtube.com/playlist?list=123", path=str(target_dir))
        folder = handler.create_playlist_folder("My Playlist")

        # Verify folder is inside target_dir, not CWD
        assert folder == str(target_dir / "My Playlist")
        assert os.path.isdir(folder)

    def test_extract_video_data(self):
        video = {"title": "Sample: Video!", "id": "abc12345"}
        title, vid = PlaylistHandler._extract_video_data(video)
        assert title == "Sample_ Video!"
        assert vid == "abc12345"

        none_title, none_vid = PlaylistHandler._extract_video_data(None)
        assert none_title == "download"
        assert none_vid == ""

    def test_clean_downloaded_title(self):
        assert PlaylistHandler._clean_downloaded_title("song_audio.mp3") == "song"
        assert PlaylistHandler._clean_downloaded_title("movie_1080p.mp4") == "movie"
        assert PlaylistHandler._clean_downloaded_title("clip_720p.mkv") == "clip"

    def test_check_for_downloaded_videos_all_existing_raises_cancelled(self, tmp_path):
        handler = PlaylistHandler(url="https://youtube.com/playlist?list=123", path=str(tmp_path))
        folder = tmp_path / "My_Playlist"
        folder.mkdir()
        (folder / "Video_1_1080p.mp4").write_text("existing")

        handler.playlist_videos = [("Video_1", "vid1")]
        with pytest.raises(DownloadCancelledError):
            handler.check_for_downloaded_videos("My_Playlist", 1)

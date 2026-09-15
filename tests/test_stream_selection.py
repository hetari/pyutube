"""Unit tests for FormatFilter and StreamSelectionService."""

import pytest

from pyutube.core.exceptions import DownloadCancelledError, NoStreamAvailableError
from pyutube.services.models import FormatInfo, VideoInfo
from pyutube.services.StreamSelectionService import FormatFilter, StreamSelectionService


class TestFormatFilter:
    def test_format_playback_priority(self):
        h264_fmt: FormatInfo = {"vcodec": "avc1.640028", "ext": "mp4", "filesize": 1000, "tbr": 500.0}
        vp9_fmt: FormatInfo = {"vcodec": "vp9", "ext": "webm", "filesize": 1200, "tbr": 600.0}
        other_mp4: FormatInfo = {"vcodec": "other", "ext": "mp4", "filesize": 800, "tbr": 400.0}

        p1 = FormatFilter.format_playback_priority(h264_fmt)
        p2 = FormatFilter.format_playback_priority(vp9_fmt)
        p3 = FormatFilter.format_playback_priority(other_mp4)

        assert p1[0] == 2  # AVC1 priority 2
        assert p3[0] == 1  # MP4 ext priority 1
        assert p2[0] == 0  # webm/other priority 0

    def test_available_video_formats(self):
        formats: list[FormatInfo] = [
            {"format_id": "137", "vcodec": "avc1.640028", "acodec": "none", "height": 1080, "filesize": 5000},
            {"format_id": "248", "vcodec": "vp9", "acodec": "none", "height": 1080, "filesize": 4000},
            {"format_id": "136", "vcodec": "avc1.4d401f", "acodec": "none", "height": 720, "filesize": 3000},
        ]
        available = FormatFilter.available_video_formats(formats)
        assert len(available) == 2
        # For 1080p, avc1 format (137) should be selected
        f1080 = [f for f in available if f.get("height") == 1080][0]
        assert f1080["format_id"] == "137"

    def test_best_audio_format(self):
        formats: list[FormatInfo] = [
            {"format_id": "140", "acodec": "mp4a.40.2", "vcodec": "none", "abr": 128.0, "filesize": 2000},
            {"format_id": "251", "acodec": "opus", "vcodec": "none", "abr": 160.0, "filesize": 2500},
        ]
        best_audio = FormatFilter.best_audio_format(formats)
        assert best_audio is not None
        assert best_audio["format_id"] == "251"

    def test_find_stream_at_or_below_height(self):
        streams: list[FormatInfo] = [
            {"format_id": "136", "vcodec": "avc1", "ext": "mp4", "height": 720},
            {"format_id": "137", "vcodec": "avc1", "ext": "mp4", "height": 1080},
        ]
        match = FormatFilter.find_stream_at_or_below_height(streams, "720p")
        assert match is not None
        assert match["format_id"] == "136"

        match_higher = FormatFilter.find_stream_at_or_below_height(streams, "1440p")
        assert match_higher is not None
        assert match_higher["format_id"] == "137"

        match_none = FormatFilter.find_stream_at_or_below_height(streams, "480p")
        assert match_none is None


class TestStreamSelectionService:
    def test_get_available_resolutions(self):
        video: VideoInfo = {
            "id": "abc",
            "title": "Test Video",
            "fulltitle": "Test Video Full",
            "formats": [
                {"format_id": "137", "vcodec": "avc1", "acodec": "none", "height": 1080, "filesize": 10 * 1024 * 1024},
                {"format_id": "140", "vcodec": "none", "acodec": "mp4a", "abr": 128.0, "filesize": 2 * 1024 * 1024},
            ],
        }
        service = StreamSelectionService(quality="1080p")
        avail = service.get_available_resolutions(video)
        assert "1080p" in avail.resolutions
        assert len(avail.sizes) == 1
        assert "MB" in avail.sizes[0]

    def test_no_audio_raises_error(self):
        video: VideoInfo = {
            "id": "abc",
            "title": "Test Video",
            "fulltitle": "Test Video",
            "formats": [
                {"format_id": "137", "vcodec": "avc1", "acodec": "none", "height": 1080},
            ],
        }
        service = StreamSelectionService(quality="1080p")
        with pytest.raises(NoStreamAvailableError):
            service.get_available_resolutions(video)

    def test_cancel_quality_raises_error(self):
        service = StreamSelectionService(quality="Cancel")
        with pytest.raises(DownloadCancelledError):
            service.get_video_streams("Cancel", [])

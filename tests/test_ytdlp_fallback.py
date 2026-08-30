"""Tests for YtDlpService error raising behavior."""

from unittest.mock import MagicMock, patch

import pytest
from yt_dlp.utils import DownloadError

from pyutube.services.YtDlpService import YtDlpService


def test_ytdlp_service_raises_error_directly():
    """Verify YtDlpService propagates DownloadError directly without fallback retries."""
    service = YtDlpService("https://www.youtube.com/watch?v=test", "/tmp")

    with patch("pyutube.services.YtDlpService.YoutubeDL") as mock_ydl_cls:
        mock_inst = MagicMock()
        mock_inst.download.side_effect = DownloadError("Network issue")
        mock_ydl_cls.return_value.__enter__.return_value = mock_inst

        with pytest.raises(DownloadError):
            service.download_audio("test.mp3", "mp3")

"""Tests for pyutube CLI argument parsing."""

import os
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from pyutube.cli import app

runner = CliRunner()


def test_cli_extra_args_with_dash_dash():
    """Verify pyutube parses extra yt-dlp flags after '--' correctly without assigning them to path."""
    with patch("pyutube.cli.DownloadService") as mock_download_service:
        mock_instance = MagicMock()
        mock_download_service.return_value = mock_instance
        mock_instance.download_preparing.return_value = MagicMock(
            video="video", video_audio="audio", quality="1080p", streams=[]
        )

        with patch("pyutube.cli.URLHandler") as mock_url_handler:
            mock_url_handler.return_value.validate.return_value = (True, "video")
            with patch("pyutube.cli.check_internet_connection", return_value=True):
                result = runner.invoke(
                    app, ["https://www.youtube.com/watch?v=FjMDADR6UX0", "-a", "--", "-4"]
                )

                assert result.exit_code == 0
                mock_download_service.assert_called_once()
                call_args, call_kwargs = mock_download_service.call_args
                # Check path is os.getcwd() and ytdlp_args is ['-4']
                assert call_args[1] == os.getcwd()
                assert call_kwargs["ytdlp_args"] == ["-4"]


def test_cli_extra_args_positional_flag_without_dash_dash():
    """Verify pyutube captures option flag like '-4' into ytdlp_args if passed as second arg."""
    with patch("pyutube.cli.DownloadService") as mock_download_service:
        mock_instance = MagicMock()
        mock_download_service.return_value = mock_instance
        mock_instance.download_preparing.return_value = MagicMock(
            video="video", video_audio="audio", quality="1080p", streams=[]
        )

        with patch("pyutube.cli.URLHandler") as mock_url_handler:
            mock_url_handler.return_value.validate.return_value = (True, "video")
            with patch("pyutube.cli.check_internet_connection", return_value=True):
                result = runner.invoke(
                    app, ["https://www.youtube.com/watch?v=FjMDADR6UX0", "-4", "-a"]
                )

                assert result.exit_code == 0
                mock_download_service.assert_called_once()
                call_args, call_kwargs = mock_download_service.call_args
                assert call_args[1] == os.getcwd()
                assert call_kwargs["ytdlp_args"] == ["-4"]

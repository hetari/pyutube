"""Unit tests for InternetChecker."""

from unittest.mock import MagicMock, patch

import requests

from pyutube.core.network import InternetChecker


class TestInternetChecker:
    @patch("requests.get")
    def test_is_available_true(self, mock_get):
        mock_get.return_value = MagicMock(status_code=200)
        assert InternetChecker.is_available()

    @patch("requests.get")
    def test_is_available_false(self, mock_get):
        mock_get.side_effect = requests.RequestException("No connection")
        assert not InternetChecker.is_available()

    @patch.object(InternetChecker, "is_available", return_value=True)
    def test_check_success(self, mock_is_avail):
        checker = InternetChecker()
        assert checker.check() is True

    @patch.object(InternetChecker, "is_available", return_value=False)
    def test_check_failure(self, mock_is_avail):
        checker = InternetChecker()
        assert checker.check() is False

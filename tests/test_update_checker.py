"""Unit tests for UpdateChecker."""

from unittest.mock import MagicMock, patch

from pyutube.core.update_checker import UpdateChecker


class TestUpdateChecker:
    def test_version_key(self):
        checker = UpdateChecker()
        assert checker._version_key("1.6.21") == (1, 6, 21)
        assert checker._version_key("2026.03.17") == (2026, 3, 17)

    def test_should_upgrade(self):
        checker = UpdateChecker()
        assert checker._should_upgrade("1.7.0", "1.6.21")
        assert not checker._should_upgrade("1.6.21", "1.6.21")
        assert not checker._should_upgrade("1.6.20", "1.6.21")

    @patch("requests.get")
    def test_fetch_latest_version_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"info": {"version": "1.7.0"}}
        mock_get.return_value = mock_response

        checker = UpdateChecker()
        latest = checker._fetch_latest_version("pyutube")
        assert latest == "1.7.0"

    @patch("requests.get")
    def test_fetch_latest_version_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        checker = UpdateChecker()
        latest = checker._fetch_latest_version("pyutube")
        assert latest is None

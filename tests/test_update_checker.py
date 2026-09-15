"""Unit tests for UpdateChecker."""

from unittest.mock import MagicMock, patch

from pyutube.core.update_checker import UpdateChecker
from pyutube.version import __version__


class TestUpdateChecker:
    def test_version_key(self):
        checker = UpdateChecker()
        expected_tuple = tuple(int(part) for part in __version__.split(".") if part.isdigit())
        assert checker._version_key(__version__) == expected_tuple
        assert checker._version_key("2026.03.17") == (2026, 3, 17)

    def test_should_upgrade(self):
        checker = UpdateChecker()
        parts = list(checker._version_key(__version__))
        higher_version = ".".join(map(str, [parts[0] + 1] + parts[1:]))
        lower_version = ".".join(map(str, parts[:-1] + [max(0, parts[-1] - 1)]))

        assert checker._should_upgrade(higher_version, __version__)
        assert not checker._should_upgrade(__version__, __version__)
        assert not checker._should_upgrade(lower_version, __version__)

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

"""Tests for pyutube error handling and diagnostics."""

import io
from unittest.mock import patch

from pyutube.core.errors import handle_error
from pyutube.ui import error_console


def test_handle_error_output():
    """Verify handle_error prints environment details, exception info, context, and traceback."""
    buffer = io.StringIO()
    test_exception = RuntimeError("Test error message")

    with patch.object(error_console, "_file", buffer):
        try:
            raise test_exception
        except RuntimeError as err:
            handle_error(err, context="Unit Test Execution")

    output = buffer.getvalue()

    assert "Error Report" in output
    assert "An unexpected error occurred!" in output
    assert "Context: Unit Test Execution" in output
    assert "Pyutube Version:" in output
    assert "yt-dlp Version:" in output
    assert "Python Version:" in output
    assert "OS / Platform:" in output
    assert "Exception Type:    RuntimeError" in output
    assert "Exception Message: Test error message" in output
    assert "Traceback:" in output
    assert "https://github.com/Hetari/pyutube/issues" in output


def test_handle_error_vpn_hint():
    """Verify handle_error includes a VPN hint for network errors."""
    buffer = io.StringIO()
    test_exception = RuntimeError("Network is unreachable")

    with patch.object(error_console, "_file", buffer):
        try:
            raise test_exception
        except RuntimeError as err:
            handle_error(err, context="Network Test Execution")

    output = " ".join(buffer.getvalue().split())
    assert (
        "Hint: If you are experiencing connection or network issues, try opening a VPN and trying again. If the issue happens again while the VPN is open, please report the bug."
        in output
    )

from unittest.mock import Mock

import pytest

from pyutube.handlers.URLHandler import URLHandler


def test_url_handler_validate_success_and_invalid(monkeypatch):
    import importlib

    url_module = importlib.import_module("pyutube.handlers.URLHandler")
    handler = URLHandler("dQw4w9WgXcQ")
    is_valid, link_type = handler.validate()

    assert is_valid is True
    assert link_type == "video"
    assert handler.url == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    error_print = Mock()
    monkeypatch.setattr(url_module.error_console, "print", error_print)
    invalid_handler = URLHandler("https://example.com")

    with pytest.raises(SystemExit):
        invalid_handler.validate()

    error_print.assert_called_once()

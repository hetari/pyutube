from types import SimpleNamespace
from unittest.mock import Mock

from pyutube.core.network import InternetChecker


def test_network_checker_success_and_failure(monkeypatch):
    get_mock = Mock(return_value=SimpleNamespace())
    monkeypatch.setattr("pyutube.core.network.requests.get", get_mock)
    monkeypatch.setattr("pyutube.core.network.console.print", Mock())
    monkeypatch.setattr("pyutube.core.network.error_console.print", Mock())

    checker = InternetChecker()
    assert checker.check() is True

    monkeypatch.setattr(
        "pyutube.core.network.requests.get",
        Mock(side_effect=__import__("requests").RequestException("offline")),
    )
    assert checker.is_available() is False

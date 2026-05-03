from types import SimpleNamespace
from unittest.mock import Mock

from pyutube.core.update_checker import PackageVersion, UpdateChecker


def test_update_checker_fetch_latest_version_and_upgrade(monkeypatch):
    checker = UpdateChecker()
    checker.packages = {"demo": PackageVersion("demo", "1.0")}

    response = SimpleNamespace(
        status_code=200,
        json=lambda: {"info": {"version": "2.0"}},
    )
    get_mock = Mock(return_value=response)
    call_mock = Mock(return_value=0)
    monkeypatch.setattr("pyutube.core.update_checker.requests.get", get_mock)
    monkeypatch.setattr("pyutube.core.update_checker.subprocess.check_call", call_mock)
    monkeypatch.setattr("pyutube.core.update_checker.console.print", Mock())
    monkeypatch.setattr("pyutube.core.update_checker.error_console.print", Mock())

    checker.check_for_updates()

    get_mock.assert_called_once()
    call_mock.assert_called_once()


def test_update_checker_skips_downgrade(monkeypatch):
    checker = UpdateChecker()
    checker.packages = {"demo": PackageVersion("demo", "1.5.1")}

    response = SimpleNamespace(
        status_code=200,
        json=lambda: {"info": {"version": "1.5.0"}},
    )
    get_mock = Mock(return_value=response)
    call_mock = Mock(return_value=0)
    monkeypatch.setattr("pyutube.core.update_checker.requests.get", get_mock)
    monkeypatch.setattr("pyutube.core.update_checker.subprocess.check_call", call_mock)
    monkeypatch.setattr("pyutube.core.update_checker.console.print", Mock())
    monkeypatch.setattr("pyutube.core.update_checker.error_console.print", Mock())

    checker.check_for_updates()

    get_mock.assert_called_once()
    call_mock.assert_not_called()


def test_update_checker_handles_http_error_and_exception(monkeypatch):
    checker = UpdateChecker()
    checker.packages = {"demo": PackageVersion("demo", "1.0")}

    response = SimpleNamespace(status_code=500, json=lambda: {"info": {"version": "2.0"}})
    get_mock = Mock(return_value=response)
    error_print = Mock()
    monkeypatch.setattr("pyutube.core.update_checker.requests.get", get_mock)
    monkeypatch.setattr("pyutube.core.update_checker.error_console.print", error_print)
    monkeypatch.setattr("pyutube.core.update_checker.console.print", Mock())

    assert checker._fetch_latest_version("demo") is None
    error_print.assert_called_once()

    monkeypatch.setattr(
        "pyutube.core.update_checker.requests.get",
        Mock(side_effect=RuntimeError("boom")),
    )
    checker.check_for_updates()

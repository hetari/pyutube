from unittest.mock import Mock

import pytest

from pyutube.services.FileConflictResolver import FileConflictResolver


def test_file_conflict_resolver_paths(monkeypatch):
    file_service = Mock()
    file_service.is_file_exists.return_value = False
    resolver = FileConflictResolver(file_service)
    assert resolver.resolve(object(), "demo.mp4", "/tmp", False) == "demo.mp4"

    file_service.is_file_exists.return_value = True
    monkeypatch.setattr("pyutube.services.FileConflictResolver.ask_rename_file", lambda filename: None)
    with pytest.raises(SystemExit):
        resolver.resolve(object(), "demo.mp4", "/tmp", False)

    monkeypatch.setattr("pyutube.services.FileConflictResolver.ask_rename_file", lambda filename: "rename")
    monkeypatch.setattr("builtins.input", lambda prompt: "")
    with pytest.raises(SystemExit):
        resolver.resolve(object(), "demo.mp4", "/tmp", False)

    monkeypatch.setattr("pyutube.services.FileConflictResolver.ask_rename_file", lambda filename: "Skip")
    assert resolver.resolve(object(), "demo.mp4", "/tmp", False) is None


def test_file_conflict_resolver_renames_existing_file(monkeypatch):
    video = object()
    file_service = Mock()
    file_service.is_file_exists.return_value = True
    file_service.generate_filename.return_value = "renamed.mp3"

    resolver = FileConflictResolver(file_service)
    monkeypatch.setattr(
        "pyutube.services.FileConflictResolver.ask_rename_file",
        lambda filename: "Rename it",
    )
    monkeypatch.setattr("builtins.input", lambda prompt: "new name")

    result = resolver.resolve(video, "old.mp3", "/tmp", True)

    assert result == "renamed.mp3"
    file_service.generate_filename.assert_called_once_with(video, True, "new name")


def test_file_conflict_resolver_cancel_exits(monkeypatch):
    file_service = Mock()
    file_service.is_file_exists.return_value = True
    resolver = FileConflictResolver(file_service)
    monkeypatch.setattr(
        "pyutube.services.FileConflictResolver.ask_rename_file",
        lambda filename: "Cancel",
    )

    with pytest.raises(SystemExit):
        resolver.resolve(object(), "old.mp3", "/tmp", True)

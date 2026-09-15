"""Unit tests for FileConflictResolver."""

from unittest.mock import MagicMock

import pytest

from pyutube.core.exceptions import DownloadCancelledError, InvalidInputError
from pyutube.core.prompts import PromptService
from pyutube.services.FileConflictResolver import FileConflictResolver


class TestFileConflictResolver:
    def test_resolve_no_collision(self, tmp_path):
        resolver = FileConflictResolver()
        result = resolver.resolve({"title": "Test"}, "test.mp4", str(tmp_path), is_audio=False)
        assert result == "test.mp4"

    def test_resolve_skip(self, tmp_path):
        existing_file = tmp_path / "test.mp4"
        existing_file.write_text("existing")

        mock_prompts = MagicMock(spec=PromptService)
        mock_prompts.ask_rename_file.return_value = "Skip"

        resolver = FileConflictResolver(prompt_service=mock_prompts)
        result = resolver.resolve({"title": "Test"}, "test.mp4", str(tmp_path), is_audio=False)
        assert result is None

    def test_resolve_cancel(self, tmp_path):
        existing_file = tmp_path / "test.mp4"
        existing_file.write_text("existing")

        mock_prompts = MagicMock(spec=PromptService)
        mock_prompts.ask_rename_file.return_value = "Cancel"

        resolver = FileConflictResolver(prompt_service=mock_prompts)
        with pytest.raises(DownloadCancelledError):
            resolver.resolve({"title": "Test"}, "test.mp4", str(tmp_path), is_audio=False)

    def test_resolve_rename(self, tmp_path, monkeypatch):
        existing_file = tmp_path / "test.mp4"
        existing_file.write_text("existing")

        mock_prompts = MagicMock(spec=PromptService)
        mock_prompts.ask_rename_file.return_value = "Rename it"

        resolver = FileConflictResolver(prompt_service=mock_prompts)
        monkeypatch.setattr(resolver, "prompt_new_filename", lambda fn: "new_name")

        result = resolver.resolve({"title": "Test", "height": 720}, "test.mp4", str(tmp_path), is_audio=False)
        assert result == "new_name_720p.mp4"

    def test_resolve_rename_empty_raises_error(self, tmp_path, monkeypatch):
        existing_file = tmp_path / "test.mp4"
        existing_file.write_text("existing")

        mock_prompts = MagicMock(spec=PromptService)
        mock_prompts.ask_rename_file.return_value = "Rename it"

        resolver = FileConflictResolver(prompt_service=mock_prompts)
        monkeypatch.setattr(resolver, "prompt_new_filename", lambda fn: "")

        with pytest.raises(InvalidInputError):
            resolver.resolve({"title": "Test"}, "test.mp4", str(tmp_path), is_audio=False)

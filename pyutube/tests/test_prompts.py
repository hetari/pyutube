from types import SimpleNamespace
from unittest.mock import Mock

from pyutube.core.prompts import PromptService


def test_prompt_service_file_type(monkeypatch):
    service = PromptService()
    question = SimpleNamespace(name="file_type")
    monkeypatch.setattr("pyutube.core.prompts.inquirer.prompt", lambda questions: {"file_type": "Audio"})

    assert service._prompt_choice(question) == "Audio"


def test_prompt_service_ask_resolution(monkeypatch):
    service = PromptService()
    monkeypatch.setattr(
        "pyutube.core.prompts.inquirer.prompt",
        lambda questions: {"resolution": "720p ~= 720p"},
    )

    assert service.ask_resolution(["720p"], ["720p"]) == "720p"


def test_prompt_service_cancel_and_audio_selection(monkeypatch):
    service = PromptService()
    monkeypatch.setattr("pyutube.core.prompts.inquirer.prompt", lambda questions: {"file_type": "Cancel"})

    assert service.asking_video_or_audio() is None

    monkeypatch.setattr("pyutube.core.prompts.inquirer.prompt", lambda questions: {"file_type": "Audio"})
    assert service.asking_video_or_audio() is True


def test_prompt_service_playlist_and_confirm(monkeypatch):
    service = PromptService()
    printed = Mock()
    monkeypatch.setattr("pyutube.core.prompts.console.print", printed)
    monkeypatch.setattr(
        "pyutube.core.prompts.inquirer.prompt",
        lambda questions: {"rename": "Overwrite it"},
    )

    assert service.ask_rename_file("demo.mp4") == "Overwrite it"

    monkeypatch.setattr(
        "pyutube.core.prompts.inquirer.prompt",
        lambda questions: {"names": ["video-1", "video-2"]},
    )
    assert service.ask_playlist_video_names(["video-1", "video-2"]) == ["video-1", "video-2"]

    monkeypatch.setattr(
        "pyutube.core.prompts.inquirer.prompt",
        lambda questions: {"ask_for_make_playlist_in_order": True},
    )
    assert service.ask_for_make_playlist_in_order() is True
    printed.assert_called_once()

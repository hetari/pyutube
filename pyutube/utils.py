"""Compatibility helpers for the pyutube package.

This module now acts as a façade over smaller, focused modules so the public
imports used by the CLI, setup script, and tests continue to work.
"""

import os

from pyutube.core.network import InternetChecker
from pyutube.core.prompts import PromptService
from pyutube.core.update_checker import UpdateChecker
from pyutube.core.url_parser import (
    is_youtube_link as _is_youtube_link,
)
from pyutube.core.url_parser import (
    is_youtube_video as _is_youtube_video,
)
from pyutube.ui import console as _console
from pyutube.ui import error_console as _error_console
from pyutube.version import __version__ as _version

__app__ = "pyutube"
ABORTED_PREFIX = "Aborted"
CANCEL_PREFIX = "Cancel"
console = _console
error_console = _error_console
__version__ = _version

_prompt_service = PromptService()
_update_checker = UpdateChecker()
_internet_checker = InternetChecker()


def clear() -> None:
    """Clear the terminal screen on the current platform."""
    os.system("cls" if os.name == "nt" else "clear")


def file_type():
    return _prompt_service.file_type()


def ask_resolution(resolutions, sizes):
    return _prompt_service.ask_resolution(resolutions, sizes)


def ask_rename_file(filename: str):
    return _prompt_service.ask_rename_file(filename)


def ask_playlist_video_names(videos):
    return _prompt_service.ask_playlist_video_names(videos)


def ask_for_make_playlist_in_order():
    return _prompt_service.ask_for_make_playlist_in_order()


def asking_video_or_audio():
    return _prompt_service.asking_video_or_audio()


def check_for_updates() -> None:
    _update_checker.check_for_updates()


def check_internet_connection() -> bool:
    return _internet_checker.check()


def is_youtube_link(link: str):
    return _is_youtube_link(link)


def is_youtube_video(link: str):
    return _is_youtube_video(link)

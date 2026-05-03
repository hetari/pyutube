"""Resolve filename conflicts before a download starts."""

import sys
from typing import Any, Optional

from termcolor import colored

from pyutube.services.FileService import FileService
from pyutube.ui import console, error_console
from pyutube.utils import ask_rename_file


class FileConflictResolver:
    """Handle overwrite, rename, and cancel decisions for existing files."""

    def __init__(self, file_service: Optional[Any] = None) -> None:
        self.file_service = file_service or FileService()

    def resolve(
        self,
        video: Any,
        filename: str,
        path: str,
        is_audio: bool = False,
    ) -> str:
        """Return a safe filename, prompting only when a collision exists."""
        if not self.file_service.is_file_exists(path, filename):
            return filename

        choice = ask_rename_file(filename)
        if choice is None:
            console.print("Download canceled", style="info")
            sys.exit()

        choice = choice.lower()
        if choice.startswith("rename"):
            new_filename = self.prompt_new_filename(filename)
            if not new_filename:
                error_console.print("Invalid filename")
                sys.exit(1)

            return self.file_service.generate_filename(video, is_audio, new_filename)

        if choice.startswith("cancel"):
            console.print("Download canceled", style="info")
            sys.exit()

        return filename

    @staticmethod
    def prompt_new_filename(filename: str) -> str:
        """Ask for a replacement filename."""
        text = colored(filename, "yellow")
        return input(f"Rename {text} to: ")

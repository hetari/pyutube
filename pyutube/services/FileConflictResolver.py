"""Resolve filename conflicts before a download starts."""

from typing import Optional

from termcolor import colored

from pyutube.core.exceptions import DownloadCancelledError, InvalidInputError
from pyutube.core.prompts import PromptService
from pyutube.services.FileService import FileService
from pyutube.services.models import VideoInfo
from pyutube.ui import console


class FileConflictResolver:
    """Handle overwrite, rename, and cancel decisions for existing files."""

    def __init__(
        self,
        file_service: Optional[FileService] = None,
        prompt_service: Optional[PromptService] = None,
    ) -> None:
        self.file_service = file_service or FileService()
        self.prompt_service = prompt_service or PromptService()

    def resolve(
        self,
        video: VideoInfo,
        filename: str,
        path: str,
        is_audio: bool = False,
    ) -> Optional[str]:
        """Return a safe filename, prompting only when a collision exists."""
        if not self.file_service.is_file_exists(path, filename):
            return filename

        choice = self.prompt_service.ask_rename_file(filename)
        if choice is None:
            raise DownloadCancelledError("Download canceled by user.")

        choice = choice.lower()
        if choice.startswith("rename"):
            new_filename = self.prompt_new_filename(filename)
            if not new_filename:
                raise InvalidInputError("Invalid filename provided.")

            return self.file_service.generate_filename(video, is_audio, new_filename)

        if choice.startswith("skip"):
            media_type = "audio" if is_audio else "video"
            console.print(f"Skipping existing {media_type} file", style="info")
            return None

        if choice.startswith("cancel"):
            raise DownloadCancelledError("Download canceled by user.")

        return filename

    @staticmethod
    def prompt_new_filename(filename: str) -> str:
        """Ask for a replacement filename."""
        text = colored(filename, "yellow")
        return input(f"Rename {text} to: ")

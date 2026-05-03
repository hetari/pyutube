import os
import sys

from pytubefix import YouTube
from pytubefix.helpers import safe_filename
from termcolor import colored

from pyutube.utils import ask_rename_file, console, error_console


class FileService:
    def save_file(self, media: YouTube, filename: str, path: str) -> None:
        """Download the selected stream to the target path."""
        media.download(output_path=path, filename=filename)

    def generate_filename(self, media, is_audio: bool = False, filename: str = ""):
        """Build a filename from the stream metadata."""
        file_type = "audio" if is_audio else media.resolution
        extension = ".m4a" if is_audio else f".{media.mime_type.split('/')[1]}"
        title = filename if filename else media.default_filename.split(".")[0]
        title = safe_filename(title)

        return f"{title}_{file_type}{extension}"

    def handle_existing_file(
        self,
        video: YouTube,
        filename: str,
        path: str,
        is_audio: bool = False,
    ) -> str:
        """Resolve filename collisions before downloading."""
        if not self.is_file_exists(path, filename):
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

            return self.generate_filename(video, is_audio, new_filename)

        if choice.startswith("cancel"):
            console.print("Download canceled", style="info")
            sys.exit()

        return filename

    def prompt_new_filename(self, filename: str) -> str:
        """Ask for a replacement filename."""
        text = colored(filename, "yellow")
        return input(f"Rename {text} to: ")

    @staticmethod
    def is_file_exists(path: str, filename: str) -> bool:
        """Return ``True`` when a file already exists on disk."""
        return os.path.isfile(os.path.join(path, filename))

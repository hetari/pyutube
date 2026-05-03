import os

from pytubefix import YouTube
from pytubefix.helpers import safe_filename


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

    @staticmethod
    def is_file_exists(path: str, filename: str) -> bool:
        """Return ``True`` when a file already exists on disk."""
        return os.path.isfile(os.path.join(path, filename))

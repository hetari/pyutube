import os
from typing import Any

from pyutube.utils import safe_filename


class FileService:
    def save_file(self, media: Any, filename: str, path: str) -> None:
        """Download the selected stream to the target path."""
        media.download(output_path=path, filename=filename)

    def generate_filename(
        self,
        media: Any,
        is_audio: bool = False,
        filename: str = "",
        audio_format: str = "wav",
        title: str = "",
    ):
        """Build a filename from the stream metadata."""
        title = filename or title or self._media_title(media)
        title = safe_filename(title)

        if is_audio:
            return f"{title}_audio.{audio_format}"

        resolution = self._media_resolution(media)
        return f"{title}_{resolution}.mp4"

    @staticmethod
    def is_file_exists(path: str, filename: str) -> bool:
        """Return ``True`` when a file already exists on disk."""
        return os.path.isfile(os.path.join(path, filename))

    @staticmethod
    def _media_title(media: Any) -> str:
        if isinstance(media, dict):
            return (
                media.get("title")
                or media.get("fulltitle")
                or media.get("id")
                or "download"
            )

        return (
            getattr(media, "title", None)
            or getattr(media, "default_filename", "")
            or "download"
        )

    @staticmethod
    def _media_resolution(media: Any) -> str:
        if isinstance(media, dict):
            height = media.get("height")
            if height:
                return f"{height}p"

            resolution = media.get("resolution")
            if resolution:
                return resolution

            return media.get("format_id") or "video"

        return getattr(media, "resolution", None) or "video"

"""File I/O and naming helpers for downloaded media."""

import os
from typing import Any, Mapping, Optional, Union

from pyutube.services.models import FormatInfo, VideoInfo
from pyutube.utils import safe_filename


class FileService:
    """Generate filenames and check file existence on disk."""

    def generate_filename(
        self,
        media: Optional[Union[FormatInfo, VideoInfo, Mapping[str, Any]]] = None,
        is_audio: bool = False,
        filename: str = "",
        title: str = "",
    ) -> str:
        """Build a filesystem-safe filename from stream or video metadata."""
        title = filename or title or self._media_title(media)
        title = safe_filename(title)

        if is_audio:
            return f"{title}_audio.mp3"

        resolution = self._media_resolution(media)
        return f"{title}_{resolution}.mp4"

    @staticmethod
    def is_file_exists(path: str, filename: str) -> bool:
        """Return ``True`` when a file already exists on disk."""
        return os.path.isfile(os.path.join(path, filename))

    @staticmethod
    def _media_title(media: Optional[Union[FormatInfo, VideoInfo, Mapping[str, Any]]]) -> str:
        if isinstance(media, (dict, Mapping)):
            return (
                str(media.get("title")
                or media.get("fulltitle")
                or media.get("id")
                or "download")
            )

        return (
            getattr(media, "title", None)
            or getattr(media, "default_filename", "")
            or "download"
        )

    @staticmethod
    def _media_resolution(media: Optional[Union[FormatInfo, VideoInfo, Mapping[str, Any]]]) -> str:
        if isinstance(media, (dict, Mapping)):
            height = media.get("height")
            if height:
                return f"{height}p"

            resolution = media.get("resolution")
            if resolution:
                return str(resolution)

            return str(media.get("format_id") or "video")

        return getattr(media, "resolution", None) or "video"

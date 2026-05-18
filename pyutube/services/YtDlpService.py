"""Helpers built on top of yt-dlp."""

import os
from typing import Any, Dict, List, Optional

from yt_dlp import YoutubeDL


class YtDlpService:
    """Thin wrapper around yt-dlp extraction and download calls."""

    def __init__(self, url: str, path: str) -> None:
        self.url = url
        self.path = path

    def extract_info(self, noplaylist: bool = True) -> Dict[str, Any]:
        """Return yt-dlp metadata for the configured URL."""
        options = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "noplaylist": noplaylist,
        }

        with YoutubeDL(options) as ydl:
            return ydl.extract_info(self.url, download=False)

    @staticmethod
    def _download_options(
        output_stem: str,
        *,
        format_selector: str,
        merge_output_format: Optional[str] = None,
        postprocessors: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        options: Dict[str, Any] = {
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
            "outtmpl": {"default": output_stem + ".%(ext)s"},
            "format": format_selector,
        }

        if merge_output_format:
            options["merge_output_format"] = merge_output_format

        if postprocessors:
            options["postprocessors"] = postprocessors

        return options

    def download_video(self, output_path: str, format_id: str) -> None:
        """Download a selected video format and merge the best audio track."""
        os.makedirs(self.path, exist_ok=True)
        output_stem, _ = os.path.splitext(output_path)
        output_stem = os.path.join(self.path, output_stem)
        options = self._download_options(
            output_stem,
            format_selector=f"{format_id}+bestaudio/best",
            merge_output_format="mp4",
        )

        with YoutubeDL(options) as ydl:
            ydl.download([self.url])

    def download_audio(self, output_path: str, audio_format: str) -> None:
        """Download the best audio track and transcode it to the target format."""
        os.makedirs(self.path, exist_ok=True)
        output_stem, _ = os.path.splitext(output_path)
        output_stem = os.path.join(self.path, output_stem)
        options = self._download_options(
            output_stem,
            format_selector="bestaudio/best",
            postprocessors=[
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": audio_format,
                }
            ],
        )

        with YoutubeDL(options) as ydl:
            ydl.download([self.url])

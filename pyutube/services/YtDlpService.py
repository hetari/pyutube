"""Helpers built on top of yt-dlp."""

import os
from typing import Any, Dict, List, Optional

from yt_dlp import YoutubeDL, parse_options


class YtDlpService:
    """Thin wrapper around yt-dlp extraction and download calls."""

    def __init__(
        self,
        url: str,
        path: str,
        ytdlp_args: Optional[List[str]] = None,
    ) -> None:
        self.url = url
        self.path = path
        self.ytdlp_args = list(ytdlp_args or [])

    @staticmethod
    def _parsed_options(ytdlp_args: Optional[List[str]]) -> Dict[str, Any]:
        if not ytdlp_args:
            return {}

        parsed = parse_options(ytdlp_args)
        return dict(parsed.ydl_opts)

    @staticmethod
    def _apply_pyutube_defaults(options: Dict[str, Any]) -> Dict[str, Any]:
        if options.get("verbose"):
            options["quiet"] = False
            options["no_warnings"] = False
        else:
            options["quiet"] = True
            options["no_warnings"] = True

        return options

    def _base_options(self) -> Dict[str, Any]:
        options = self._parsed_options(self.ytdlp_args)
        return self._apply_pyutube_defaults(options)

    def extract_info(self, noplaylist: bool = True) -> Dict[str, Any]:
        """Return yt-dlp metadata for the configured URL."""
        options = self._base_options()
        options.update(
            {
                "skip_download": True,
                "noplaylist": noplaylist,
            }
        )

        with YoutubeDL(options) as ydl:
            return ydl.extract_info(self.url, download=False)

    def _download_options(
        self,
        output_stem: str,
        *,
        format_selector: str,
        merge_output_format: Optional[str] = None,
        postprocessors: Optional[List[Dict[str, Any]]] = None,
        extra_options: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        options = self._base_options()
        options.update(
            {
                "noplaylist": True,
                "outtmpl": {"default": output_stem + ".%(ext)s"},
            }
        )

        if extra_options:
            options.update(extra_options)

        if "format" not in options or not options["format"]:
            options["format"] = format_selector

        if merge_output_format and not options.get("merge_output_format"):
            options["merge_output_format"] = merge_output_format

        if postprocessors and not options.get("postprocessors"):
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

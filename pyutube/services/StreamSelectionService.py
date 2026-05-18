"""Select and describe the video streams available for download."""

import sys
from typing import Any

from termcolor import colored
from yaspin import yaspin
from yaspin.spinners import Spinners

from pyutube.services.models import AvailableVideoStreams, DownloadPreparation
from pyutube.ui import error_console
from pyutube.utils import CANCEL_PREFIX, ask_resolution


class StreamSelectionService:
    """Inspect streams and resolve the quality the user wants."""

    def __init__(self, quality: str) -> None:
        self.quality = quality

    @yaspin(text=colored("getting media streams", "green"), spinner=Spinners.point)
    def get_available_resolutions(self, video: Any) -> AvailableVideoStreams:
        """Return resolution labels, sizes, and the related formats."""
        formats = video.get("formats") or []
        available_streams = self._available_video_formats(formats)
        audio_stream = self._best_audio_format(formats)
        if audio_stream is None:
            error_console.print("No audio stream was found for this video.")
            sys.exit(1)

        resolutions_with_sizes = self.get_video_resolutions_sizes(
            available_streams,
            audio_stream,
        )
        if not resolutions_with_sizes:
            error_console.print("No downloadable video streams were found.")
            sys.exit(1)

        resolutions_with_sizes = sorted(
            resolutions_with_sizes,
            key=self._resolution_sort_key,
        )

        resolutions, sizes = zip(*resolutions_with_sizes)
        return AvailableVideoStreams(
            resolutions=list(resolutions),
            sizes=list(sizes),
            streams=available_streams,
            audio_stream=audio_stream,
        )

    def get_video_streams(self, quality: str, streams: Any):
        """Pick the best matching format for the requested quality cap."""
        if quality and quality.startswith(CANCEL_PREFIX):
            error_console.print("❗ Cancel the download...")
            sys.exit()

        target_quality = self._normalize_quality(quality)

        with yaspin(
            text=colored("Downloading the video...", "green"),
            color="green",
            spinner=Spinners.dots13,
        ):
            stream = self._find_stream_at_or_below_height(streams, target_quality)

            if stream:
                return stream

            error_console.print("❗ No matching video quality was found.")
            sys.exit(1)

    def get_selected_stream(
        self,
        video: Any,
        is_audio: bool = False,
    ) -> DownloadPreparation:
        """Return the streams needed for the selected download mode."""
        available = self.get_available_resolutions(video)

        if not available.streams:
            error_console.print("❗ Cancel the download...")
            sys.exit()

        if not is_audio:
            self.quality = self.quality or ask_resolution(available.resolutions, available.sizes)
            if not self.quality or self.quality.startswith(CANCEL_PREFIX):
                error_console.print("❗ Cancel the download...")
                sys.exit()

        return DownloadPreparation(
            video=video,
            streams=available.streams,
            video_audio=available.audio_stream,
            quality=self.quality,
        )

    @staticmethod
    def get_video_resolutions_sizes(available_streams, audio_stream):
        """Return resolution labels paired with estimated file sizes."""
        if not available_streams:
            return []

        audio_filesize = (
            audio_stream.get("filesize")
            or audio_stream.get("filesize_approx")
            or 0
        )
        resolutions_with_sizes = []
        one_mb = 1024 * 1024
        one_gb = one_mb * 1024

        for stream in available_streams:
            height = stream.get("height")
            if not height:
                continue

            video_filesize_bytes = stream.get("filesize") or stream.get("filesize_approx") or 0
            if stream.get("acodec") == "none":
                video_filesize_bytes += audio_filesize

            if video_filesize_bytes >= one_gb:
                video_filesize = f"{video_filesize_bytes / one_gb:.4f} GB"
            elif video_filesize_bytes >= one_mb:
                video_filesize = f"{video_filesize_bytes / one_mb:.2f} MB"
            else:
                video_filesize = f"{video_filesize_bytes / 1024:.2f} KB"

            resolutions_with_sizes.append((f"{height}p", video_filesize))

        return resolutions_with_sizes

    @staticmethod
    def _resolution_sort_key(item):
        resolution, _ = item
        numeric_value = resolution[:-1]
        return int(numeric_value) if numeric_value.isdigit() else float("inf")

    @staticmethod
    def _normalize_quality(quality: str) -> str:
        return quality[:-1] if quality.endswith("p") else quality

    @staticmethod
    def _available_video_formats(formats):
        preferred = [
            fmt
            for fmt in formats
            if fmt.get("vcodec") != "none"
            and fmt.get("acodec") == "none"
            and fmt.get("height") is not None
        ]
        if not preferred:
            preferred = [
                fmt
                for fmt in formats
                if fmt.get("vcodec") != "none" and fmt.get("height") is not None
            ]

        unique_formats = {}
        for fmt in preferred:
            height = int(fmt["height"])
            current = unique_formats.get(height)
            if current is None:
                unique_formats[height] = fmt
                continue

            current_priority = StreamSelectionService._format_playback_priority(current)
            candidate_priority = StreamSelectionService._format_playback_priority(fmt)
            if candidate_priority > current_priority:
                unique_formats[height] = fmt
            elif candidate_priority == current_priority:
                current_size = (
                    current.get("filesize") or current.get("filesize_approx") or 0
                )
                candidate_size = (
                    fmt.get("filesize") or fmt.get("filesize_approx") or 0
                )
                if candidate_size > current_size:
                    unique_formats[height] = fmt

        return [unique_formats[key] for key in sorted(unique_formats)]

    @staticmethod
    def _format_playback_priority(fmt):
        vcodec = str(fmt.get("vcodec") or "").lower()
        ext = str(fmt.get("ext") or "").lower()

        if vcodec.startswith("avc1") or "h264" in vcodec:
            codec_priority = 2
        elif ext == "mp4":
            codec_priority = 1
        else:
            codec_priority = 0

        return codec_priority, ext == "mp4", fmt.get("filesize") or fmt.get("filesize_approx") or 0, fmt.get("tbr") or 0

    @staticmethod
    def _find_stream_at_or_below_height(streams, quality):
        try:
            target_height = int(str(quality).replace("p", ""))
        except ValueError:
            return None

        matches = [
            stream
            for stream in streams
            if stream.get("height") is not None and int(stream.get("height")) <= target_height
        ]
        if not matches:
            return None

        return max(matches, key=StreamSelectionService._stream_sort_key)

    @staticmethod
    def _stream_sort_key(fmt):
        height = int(fmt.get("height") or 0)
        return (height,) + StreamSelectionService._format_playback_priority(fmt)

    @staticmethod
    def _best_audio_format(formats):
        audio_formats = [
            fmt
            for fmt in formats
            if fmt.get("acodec") != "none" and fmt.get("vcodec") == "none"
        ]
        if not audio_formats:
            audio_formats = [
                fmt for fmt in formats if fmt.get("acodec") != "none"
            ]

        if not audio_formats:
            return None

        def sort_key(fmt):
            return (
                fmt.get("abr") or 0,
                fmt.get("tbr") or 0,
                fmt.get("filesize") or fmt.get("filesize_approx") or 0,
            )

        return max(audio_formats, key=sort_key)

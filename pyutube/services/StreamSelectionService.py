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

    @yaspin(text=colored("getting video streams", "green"), spinner=Spinners.point)
    def get_available_resolutions(self, video: Any) -> AvailableVideoStreams:
        """Return resolution labels, sizes, and the related streams."""
        streams = video.streams
        available_streams = streams.filter(
            progressive=False,
            adaptive=True,
            mime_type="video/mp4",
        )
        audio_stream = streams.filter(only_audio=True).order_by("mime_type").first()
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

    @yaspin(
        text=colored("Downloading the video...", "green"),
        color="green",
        spinner=Spinners.dots13,
    )
    def get_video_streams(self, quality: str, streams: Any):
        """Pick the best matching stream for the requested quality."""
        stream = streams.filter(res=quality).first()

        if quality and quality.startswith(CANCEL_PREFIX):
            error_console.print("❗ Cancel the download...")
            sys.exit()

        if stream:
            return stream

        available_qualities = [
            int(resolution.replace("p", ""))
            for resolution in (stream.resolution for stream in streams)
            if resolution and resolution.replace("p", "").isdigit()
        ]
        if not available_qualities:
            error_console.print("❗ No matching video quality was found.")
            sys.exit(1)

        quality_int = int(quality.replace("p", "")) if "p" in quality else int(quality)
        selected_quality = min(
            available_qualities,
            key=lambda value: abs(quality_int - value),
        )
        return streams.filter(res=f"{selected_quality}p").first()

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
            if not self.quality:
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

        audio_filesize = audio_stream.filesize
        resolutions_with_sizes = []
        one_mb = 1024 * 1024
        one_gb = one_mb * 1024

        for stream in available_streams:
            if not stream.resolution:
                continue

            video_filesize_bytes = stream.filesize
            if not stream.is_progressive:
                video_filesize_bytes += audio_filesize

            if video_filesize_bytes >= one_gb:
                video_filesize = f"{video_filesize_bytes / one_gb:.4f} GB"
            elif video_filesize_bytes >= one_mb:
                video_filesize = f"{video_filesize_bytes / one_mb:.2f} MB"
            else:
                video_filesize = f"{video_filesize_bytes / 1024:.2f} KB"

            resolutions_with_sizes.append((stream.resolution, video_filesize))

        return resolutions_with_sizes

    @staticmethod
    def _resolution_sort_key(item):
        resolution, _ = item
        numeric_value = resolution[:-1]
        return int(numeric_value) if numeric_value.isdigit() else float("inf")

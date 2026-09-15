"""Select and describe the video streams available for download."""

from typing import List, Optional, Sequence, Tuple

from termcolor import colored
from yaspin import yaspin
from yaspin.spinners import Spinners

from pyutube.core.exceptions import (
    DownloadCancelledError,
    NoStreamAvailableError,
)
from pyutube.core.prompts import PromptService
from pyutube.services.models import (
    AvailableVideoStreams,
    DownloadPreparation,
    FormatInfo,
    VideoInfo,
)
from pyutube.utils import CANCEL_PREFIX


class FormatFilter:
    """Helper utilities for filtering and scoring yt-dlp media formats."""

    @staticmethod
    def format_playback_priority(fmt: FormatInfo) -> Tuple[int, bool, int, float]:
        """Rank formats prioritizing AVC/H.264 codecs, mp4 containers, and size/bitrate."""
        vcodec = str(fmt.get("vcodec") or "").lower()
        ext = str(fmt.get("ext") or "").lower()

        if vcodec.startswith("avc1") or "h264" in vcodec:
            codec_priority = 2
        elif ext == "mp4":
            codec_priority = 1
        else:
            codec_priority = 0

        filesize = fmt.get("filesize") or fmt.get("filesize_approx") or 0
        tbr = fmt.get("tbr") or 0.0
        return codec_priority, ext == "mp4", filesize, float(tbr)

    @classmethod
    def available_video_formats(cls, formats: Sequence[FormatInfo]) -> List[FormatInfo]:
        """Find the best video format for each available resolution height."""
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

        unique_formats: dict[int, FormatInfo] = {}
        for fmt in preferred:
            height = int(fmt["height"])  # type: ignore
            current = unique_formats.get(height)
            if current is None:
                unique_formats[height] = fmt
                continue

            current_priority = cls.format_playback_priority(current)
            candidate_priority = cls.format_playback_priority(fmt)
            if candidate_priority > current_priority:
                unique_formats[height] = fmt
            elif candidate_priority == current_priority:
                current_size = current.get("filesize") or current.get("filesize_approx") or 0
                candidate_size = fmt.get("filesize") or fmt.get("filesize_approx") or 0
                if candidate_size > current_size:
                    unique_formats[height] = fmt

        return [unique_formats[key] for key in sorted(unique_formats)]

    @classmethod
    def best_audio_format(cls, formats: Sequence[FormatInfo]) -> Optional[FormatInfo]:
        """Find the highest quality audio stream available."""
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

        def sort_key(fmt: FormatInfo) -> Tuple[float, float, int]:
            return (
                float(fmt.get("abr") or 0.0),
                float(fmt.get("tbr") or 0.0),
                int(fmt.get("filesize") or fmt.get("filesize_approx") or 0),
            )

        return max(audio_formats, key=sort_key)

    @classmethod
    def find_stream_at_or_below_height(
        cls, streams: Sequence[FormatInfo], quality: str
    ) -> Optional[FormatInfo]:
        """Find the highest-ranked format at or below the target height."""
        try:
            target_height = int(str(quality).replace("p", ""))
        except ValueError:
            return None

        matches = [
            stream
            for stream in streams
            if stream.get("height") is not None and int(stream.get("height")) <= target_height  # type: ignore
        ]
        if not matches:
            return None

        def stream_sort_key(fmt: FormatInfo) -> Tuple[int, int, bool, int, float]:
            height = int(fmt.get("height") or 0)
            return (height,) + cls.format_playback_priority(fmt)

        return max(matches, key=stream_sort_key)


class StreamSelectionService:
    """Inspect streams and resolve the quality the user wants."""

    def __init__(
        self,
        quality: str,
        prompt_service: Optional[PromptService] = None,
    ) -> None:
        self.quality = quality
        self.prompt_service = prompt_service or PromptService()

    @yaspin(text=colored("getting media streams", "green"), spinner=Spinners.point)
    def get_available_resolutions(self, video: VideoInfo) -> AvailableVideoStreams:
        """Return resolution labels, sizes, and the related formats."""
        formats = video.get("formats") or []
        available_streams = FormatFilter.available_video_formats(formats)
        audio_stream = FormatFilter.best_audio_format(formats)
        if audio_stream is None:
            raise NoStreamAvailableError("No audio stream was found for this video.")

        resolutions_with_sizes = self.get_video_resolutions_sizes(
            available_streams,
            audio_stream,
        )
        if not resolutions_with_sizes:
            raise NoStreamAvailableError("No downloadable video streams were found.")

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

    def get_video_streams(self, quality: str, streams: Sequence[FormatInfo]) -> FormatInfo:
        """Pick the best matching format for the requested quality cap."""
        if quality and quality.startswith(CANCEL_PREFIX):
            raise DownloadCancelledError("User cancelled download.")

        target_quality = self._normalize_quality(quality)

        with yaspin(
            text=colored("Downloading the video...", "green"),
            color="green",
            spinner=Spinners.dots13,
        ):
            stream = FormatFilter.find_stream_at_or_below_height(streams, target_quality)

            if stream:
                return stream

            raise NoStreamAvailableError("No matching video quality was found.")

    def get_selected_stream(
        self,
        video: VideoInfo,
        is_audio: bool = False,
    ) -> DownloadPreparation:
        """Return the streams needed for the selected download mode."""
        available = self.get_available_resolutions(video)

        if not available.streams:
            raise DownloadCancelledError("No streams available, cancelling download.")

        if not is_audio:
            self.quality = self.quality or self.prompt_service.ask_resolution(
                available.resolutions, available.sizes
            )
            if not self.quality or self.quality.startswith(CANCEL_PREFIX):
                raise DownloadCancelledError("User cancelled download.")

        return DownloadPreparation(
            video=video,
            streams=available.streams,
            video_audio=available.audio_stream,
            quality=self.quality,
        )

    @staticmethod
    def get_video_resolutions_sizes(
        available_streams: Sequence[FormatInfo],
        audio_stream: Optional[FormatInfo],
    ) -> List[Tuple[str, str]]:
        """Return resolution labels paired with estimated file sizes."""
        if not available_streams:
            return []

        audio_filesize = 0
        if audio_stream:
            audio_filesize = (
                audio_stream.get("filesize")
                or audio_stream.get("filesize_approx")
                or 0
            )

        resolutions_with_sizes: List[Tuple[str, str]] = []
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
    def _resolution_sort_key(item: Tuple[str, str]) -> float:
        resolution, _ = item
        numeric_value = resolution[:-1]
        return float(int(numeric_value)) if numeric_value.isdigit() else float("inf")

    @staticmethod
    def _normalize_quality(quality: str) -> str:
        return quality[:-1] if quality.endswith("p") else quality

"""Small dataclasses used across download workflows."""

from dataclasses import dataclass
from typing import Any, List, Tuple


@dataclass
class AvailableVideoStreams:
    """Resolved stream metadata used for quality selection."""

    resolutions: List[str]
    sizes: List[str]
    streams: Any
    audio_stream: Any


@dataclass
class DownloadPreparation:
    """Ready-to-download data for a single video."""

    video: Any
    streams: Any
    video_audio: Any
    quality: str


@dataclass
class PlaylistDownloadPlan:
    """Collected playlist choices and the target download path."""

    new_path: str
    is_audio: bool
    videos_selected: List[str]
    make_in_order: bool
    playlist_videos: List[Tuple[str, str]]

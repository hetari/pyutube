"""Data models and TypedDicts used across download workflows."""

from dataclasses import dataclass
from typing import List, Optional, Tuple, TypedDict


class FormatInfo(TypedDict, total=False):
    """yt-dlp format dictionary shape."""

    format_id: str
    format_note: str
    ext: str
    vcodec: str
    acodec: str
    height: Optional[int]
    width: Optional[int]
    resolution: Optional[str]
    filesize: Optional[int]
    filesize_approx: Optional[int]
    abr: Optional[float]
    tbr: Optional[float]
    fps: Optional[float]


class VideoInfo(TypedDict, total=False):
    """yt-dlp video metadata dictionary shape."""

    id: str
    title: str
    fulltitle: str
    formats: List[FormatInfo]
    duration: Optional[int]
    thumbnail: Optional[str]
    uploader: Optional[str]


@dataclass
class AvailableVideoStreams:
    """Resolved stream metadata used for quality selection."""

    resolutions: List[str]
    sizes: List[str]
    streams: List[FormatInfo]
    audio_stream: Optional[FormatInfo]


@dataclass
class DownloadPreparation:
    """Ready-to-download data for a single video."""

    video: VideoInfo
    streams: List[FormatInfo]
    video_audio: Optional[FormatInfo]
    quality: str


@dataclass
class PlaylistDownloadPlan:
    """Collected playlist choices and the target download path."""

    new_path: str
    is_audio: bool
    videos_selected: List[str]
    make_in_order: bool
    playlist_videos: List[Tuple[str, str]]

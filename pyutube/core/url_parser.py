"""YouTube URL parsing and validation helpers."""

import re
from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class YouTubeLinkResult:
    """Parsed state for a YouTube link."""

    is_valid: bool
    link_type: str


class YouTubeURLParser:
    """Recognize and normalize the YouTube URL shapes supported by pyutube."""

    VIDEO_ID_PATTERN = re.compile(r"^[a-zA-Z0-9_-]{11}$")
    VIDEO_PATTERN = re.compile(
        r"^(?:https?://)?(?:www\.)?"
        r"(?:youtube(?:-nocookie)?\.com/(?:(?:watch\?(?:feature=share&)?v=)|embed/|v/|live_stream\?channel=|live/)"
        r"|youtu\.be/)([a-zA-Z0-9_-]{11})"
    )
    SHORTS_PATTERN = re.compile(
        r"^(?:https?://)?(?:www\.)?youtube\.com/shorts/([a-zA-Z0-9_-]+)"
    )
    PLAYLIST_PATTERN = re.compile(
        r"^(?:https?://)?(?:www\.)?youtube\.com/playlist\?list=([a-zA-Z0-9_-]+)"
    )
    WATCH_PLAYLIST_PATTERN = re.compile(
        r"^(?:https?://)?(?:www\.)?youtube\.com/watch\?v=[a-zA-Z0-9_-]{11}&list=([a-zA-Z0-9_-]+)"
    )

    def __init__(self, url: str) -> None:
        self.url = url

    @classmethod
    def is_video_id(cls, video_id: str) -> bool:
        return bool(cls.VIDEO_ID_PATTERN.match(video_id))

    @classmethod
    def is_youtube_video(cls, link: str) -> bool:
        return bool(cls.VIDEO_PATTERN.match(link))

    @classmethod
    def is_youtube_shorts(cls, link: str) -> bool:
        return bool(cls.SHORTS_PATTERN.match(link))

    @classmethod
    def is_youtube_playlist(cls, link: str) -> bool:
        return bool(cls.PLAYLIST_PATTERN.match(link)) or bool(
            cls.WATCH_PLAYLIST_PATTERN.match(link)
        )

    @classmethod
    def is_youtube_link(cls, link: str) -> Tuple[bool, str]:
        if cls.is_youtube_video(link):
            return True, "video"

        if cls.is_youtube_shorts(link):
            return True, "short"

        if cls.is_youtube_playlist(link):
            return True, "playlist"

        return False, "unknown"

    def normalize(self) -> str:
        """Return a canonical watch URL when the input is a bare video id."""
        if self.is_video_id(self.url):
            return f"https://www.youtube.com/watch?v={self.url}"

        return self.url

    def validate(self) -> Tuple[bool, str]:
        """Return the validation result for the configured URL."""
        return self.is_youtube_link(self.normalize())


def is_youtube_link(link: str) -> Tuple[bool, str]:
    """Compatibility helper for the historic function-based API."""
    return YouTubeURLParser.is_youtube_link(link)


def is_youtube_video(link: str) -> bool:
    """Compatibility helper for the historic function-based API."""
    return YouTubeURLParser.is_youtube_video(link)

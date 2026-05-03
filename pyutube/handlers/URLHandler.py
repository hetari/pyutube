import re
import sys

from pyutube.utils import error_console


class URLHandler:
    VIDEO_ID_PATTERN = re.compile(r"^[a-zA-Z0-9_-]{11}$")
    VIDEO_PATTERN = re.compile(
        r"^(?:https?://)?(?:www\.)?(?:youtube(?:-nocookie)?\.com/(?:(?:watch\?(?:feature=share&)?v=)|embed/|v/|live_stream\?channel=|live/)|youtu\.be/)([a-zA-Z0-9_-]{11})"
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

    def __init__(self, url):
        self.url = url

    def validate(self):
        if self.__is_youtube_video_id(self.url):
            self.url = f"https://www.youtube.com/watch?v={self.url}"

        return self.__validate_link(self.url)

    def __validate_link(self, url: str) -> tuple[bool, str]:
        is_valid_link, link_type = self.__is_youtube_link(url)
        if not is_valid_link:
            error_console.print("❌ Invalid link")
            sys.exit(1)

        return is_valid_link, link_type.lower()

    def __is_youtube_link(self, link: str) -> tuple[bool, str]:
        is_video = self.__is_youtube_video(link)
        if is_video:
            return True, "video"

        is_short = self.__is_youtube_shorts(link)
        if is_short:
            return True, "short"

        is_playlist = self.__is_youtube_playlist(link)
        if is_playlist:
            return True, "playlist"

        return False, "unknown"

    def __is_youtube_shorts(self, link: str) -> bool:
        return bool(self.SHORTS_PATTERN.match(link))

    def __is_youtube_video(self, link: str) -> bool:
        return bool(self.VIDEO_PATTERN.match(link))

    def __is_youtube_playlist(self, link: str) -> bool:
        return bool(self.PLAYLIST_PATTERN.match(link)) or bool(
            self.WATCH_PLAYLIST_PATTERN.match(link)
        )

    def __is_youtube_video_id(self, video_id: str) -> bool:
        return bool(self.VIDEO_ID_PATTERN.match(video_id))

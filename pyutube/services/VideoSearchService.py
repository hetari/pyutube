"""Search for a YouTube video and extract its metadata."""

from typing import Optional

from termcolor import colored
from yaspin import yaspin
from yaspin.spinners import Spinners

from pyutube.core.exceptions import NoVideoFoundError
from pyutube.core.logger import logger
from pyutube.services.models import VideoInfo
from pyutube.services.YtDlpService import YtDlpService


class VideoSearchService:
    """Create yt-dlp info dictionaries for a URL."""

    def __init__(self, url: str, ytdlp_args: Optional[list[str]] = None) -> None:
        self.url = url
        self.ytdlp_args = list(ytdlp_args or [])

    def search_process(self) -> VideoInfo:
        """Create a metadata dictionary for the current URL."""
        logger.log("VideoSearchService.search_process", {"url": self.url})
        video = self._video_search()

        if not video:
            logger.log("VideoSearchService.no_video_found", {"url": self.url})
            raise NoVideoFoundError(f"No stream available for the url: {self.url}")

        logger.log(
            "VideoSearchService.video_found",
            {"title": video.get("title"), "id": video.get("id")},
        )
        return video

    @yaspin(
        text=colored("Searching for the video", "green"),
        color="green",
        spinner=Spinners.point,
    )
    def _video_search(self) -> VideoInfo:
        return YtDlpService(self.url, "", self.ytdlp_args).extract_info(
            noplaylist=True
        )  # type: ignore

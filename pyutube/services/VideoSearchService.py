"""Search for a YouTube video."""

import sys
from typing import Any

from termcolor import colored
from yaspin import yaspin
from yaspin.spinners import Spinners

from pyutube.services.YtDlpService import YtDlpService
from pyutube.ui import error_console


class VideoSearchService:
    """Create yt-dlp info dictionaries for a URL."""

    def __init__(self, url: str) -> None:
        self.url = url

    def search_process(self) -> Any:
        """Create a metadata dictionary for the current URL."""
        try:
            video = self._video_search()
        except Exception as error:
            error_console.print(f"Error: {error}")
            sys.exit(1)

        if not video:
            error_console.print("No stream available for the url.")
            sys.exit()

        return video

    @yaspin(
        text=colored("Searching for the video", "green"),
        color="green",
        spinner=Spinners.point,
    )
    def _video_search(self) -> Any:
        return YtDlpService(self.url, "").extract_info(noplaylist=True)

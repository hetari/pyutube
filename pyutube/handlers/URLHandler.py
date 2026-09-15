"""URL validation and normalization for YouTube links."""

from typing import Tuple

from pyutube.core.exceptions import InvalidInputError
from pyutube.core.logger import logger
from pyutube.core.url_parser import YouTubeURLParser


class URLHandler:
    """Validate and normalize a YouTube URL before download."""

    def __init__(self, url: str) -> None:
        self.url = url
        self.parser = YouTubeURLParser(url)

    def validate(self) -> Tuple[bool, str]:
        logger.log("URLHandler.validate", {"url": self.url})
        self.url = self.parser.normalize()
        is_valid_link, link_type = self.parser.validate()
        logger.log(
            "URLHandler.validated",
            {"is_valid": is_valid_link, "link_type": link_type},
        )
        if not is_valid_link:
            raise InvalidInputError("Invalid YouTube link.")

        return is_valid_link, link_type.lower()

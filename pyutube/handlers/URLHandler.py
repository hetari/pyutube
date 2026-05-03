import sys

from pyutube.core.url_parser import YouTubeURLParser
from pyutube.ui import error_console


class URLHandler:
    def __init__(self, url):
        self.url = url
        self.parser = YouTubeURLParser(url)

    def validate(self):
        self.url = self.parser.normalize()
        is_valid_link, link_type = self.parser.validate()
        if not is_valid_link:
            error_console.print("❌ Invalid link")
            sys.exit(1)

        return is_valid_link, link_type.lower()

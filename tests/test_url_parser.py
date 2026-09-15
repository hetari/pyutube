"""Unit tests for YouTubeURLParser."""


from pyutube.core.url_parser import YouTubeURLParser, is_youtube_link, is_youtube_video


class TestYouTubeURLParser:
    def test_valid_video_urls(self):
        valid_urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "http://youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ",
            "https://m.youtube.com/watch?v=dQw4w9WgXcQ",
        ]
        for url in valid_urls:
            assert YouTubeURLParser.is_youtube_video(url)
            is_valid, link_type = YouTubeURLParser.is_youtube_link(url)
            assert is_valid
            assert link_type == "video"

    def test_valid_shorts_urls(self):
        shorts_url = "https://www.youtube.com/shorts/abcdef12345"
        assert YouTubeURLParser.is_youtube_shorts(shorts_url)
        is_valid, link_type = YouTubeURLParser.is_youtube_link(shorts_url)
        assert is_valid
        assert link_type == "short"

    def test_valid_playlist_urls(self):
        playlist_url = "https://www.youtube.com/playlist?list=PL1234567890abcdef"
        assert YouTubeURLParser.is_youtube_playlist(playlist_url)
        is_valid, link_type = YouTubeURLParser.is_youtube_link(playlist_url)
        assert is_valid
        assert link_type == "playlist"

    def test_invalid_urls(self):
        invalid_urls = [
            "https://google.com",
            "https://vimeo.com/123456",
            "not_a_url",
            "",
            "https://youtube.com/invalid_pattern",
        ]
        for url in invalid_urls:
            is_valid, link_type = YouTubeURLParser.is_youtube_link(url)
            assert not is_valid
            assert link_type == "unknown"

    def test_parser_instance_validation_and_normalize(self):
        url = "https://youtu.be/dQw4w9WgXcQ?si=abcdef"
        parser = YouTubeURLParser(url)
        normalized = parser.normalize()
        assert "youtu.be" in normalized
        is_valid, link_type = parser.validate()
        assert is_valid
        assert link_type == "video"

    def test_convenience_functions(self):
        assert is_youtube_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        is_valid, _ = is_youtube_link("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        assert is_valid

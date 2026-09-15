"""Unit tests for FileService and safe_filename."""

from pyutube.services.FileService import FileService
from pyutube.services.models import FormatInfo, VideoInfo
from pyutube.utils import safe_filename


class TestFileService:
    def test_safe_filename(self):
        assert safe_filename('Hello/World: "Test"?*|<>\x00') == "Hello_World_ _Test"
        assert safe_filename("Hello/World/Test") == "Hello_World_Test"
        assert safe_filename("   ...clean...   ") == "clean"
        assert safe_filename("") == "download"

    def test_generate_audio_filename(self):
        service = FileService()
        video: VideoInfo = {"id": "123", "title": "My Song"}
        filename = service.generate_filename(video, is_audio=True)
        assert filename == "My Song_audio.mp3"

    def test_generate_video_filename(self):
        service = FileService()
        fmt: FormatInfo = {"height": 1080, "ext": "mp4"}
        filename = service.generate_filename(fmt, is_audio=False, title="My Movie")
        assert filename == "My Movie_1080p.mp4"

    def test_is_file_exists(self, tmp_path):
        service = FileService()
        test_file = tmp_path / "test.mp4"
        assert not service.is_file_exists(str(tmp_path), "test.mp4")
        test_file.write_text("dummy")
        assert service.is_file_exists(str(tmp_path), "test.mp4")

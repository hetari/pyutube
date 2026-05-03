from types import SimpleNamespace
from unittest.mock import Mock

from pyutube.services.FileService import FileService


def test_file_service_helpers(tmp_path):
    file_service = FileService()
    media = SimpleNamespace(default_filename="demo.mp4", resolution="720p", mime_type="video/mp4")
    audio_media = SimpleNamespace(default_filename="track.webm", resolution="audio", mime_type="audio/mp4")

    assert file_service.generate_filename(media) == "demo_720p.mp4"
    assert file_service.generate_filename(audio_media, is_audio=True) == "track_audio.mp3"

    output = Mock()
    media.download = output
    file_service.save_file(media, "demo_720p.mp4", str(tmp_path))
    output.assert_called_once_with(output_path=str(tmp_path), filename="demo_720p.mp4")

    (tmp_path / "demo_720p.mp4").write_text("content")
    assert file_service.is_file_exists(str(tmp_path), "demo_720p.mp4") is True

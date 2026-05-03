from unittest.mock import Mock

from pyutube.services.AudioConversionService import AudioConversionService


def test_audio_conversion_service_converts_and_cleans_temp(monkeypatch, tmp_path):
    import pyutube.services.AudioConversionService as audio_module

    input_path = tmp_path / "raw.mp4"
    output_path = tmp_path / "final.mp3"
    input_path.write_text("raw-audio")

    run_mock = Mock(return_value=None)
    remove_mock = Mock()
    monkeypatch.setattr(audio_module.imageio_ffmpeg, "get_ffmpeg_exe", lambda: "/usr/bin/ffmpeg")
    monkeypatch.setattr(audio_module.subprocess, "run", run_mock)
    monkeypatch.setattr(audio_module.os.path, "exists", lambda path: path == str(input_path))
    monkeypatch.setattr(audio_module.os, "remove", remove_mock)
    monkeypatch.setattr(audio_module.console, "print", Mock())
    monkeypatch.setattr(audio_module.error_console, "print", Mock())

    service = AudioConversionService()
    result = service.convert_to_mp3(str(input_path), str(output_path))

    assert result == str(output_path)
    run_mock.assert_called_once()
    remove_mock.assert_called_once_with(str(input_path))

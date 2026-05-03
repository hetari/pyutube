from types import SimpleNamespace

from pyutube.services.AudioService import AudioService


def test_audio_service_returns_first_audio_stream():
    audio_stream = SimpleNamespace(title="audio")
    video = SimpleNamespace(
        streams=SimpleNamespace(
            filter=lambda only_audio=True: SimpleNamespace(
                order_by=lambda field: SimpleNamespace(first=lambda: audio_stream)
            )
        )
    )

    assert AudioService.get_audio_streams(video) is audio_stream

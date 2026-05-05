from pathlib import Path
from unittest.mock import Mock

from pyutube.services.VideoMergeService import VideoMergeService


def test_video_merge_service_merging_moves_output(tmp_path, monkeypatch):
    service = VideoMergeService(str(tmp_path))
    (tmp_path / "clip_720p.mp4").write_text("video")
    (tmp_path / "clip_audio.m4a").write_text("audio")

    import pyutube.services.VideoMergeService as merge_module
    merge_mock = Mock(
        side_effect=lambda v, a, o, **kwargs: Path(o).write_text("merged")
    )
    monkeypatch.setattr(merge_module, "ffmpeg_merge_video_audio", merge_mock)

    service.merging("clip_720p.mp4", "clip_audio.m4a")

    assert (tmp_path / "clip_720p.mp4").read_text() == "merged"
    assert not (tmp_path / "output").exists()
    merge_mock.assert_called_once()

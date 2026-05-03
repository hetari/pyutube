from pathlib import Path

from pyutube.services.VideoMergeService import VideoMergeService


def test_video_merge_service_merging_moves_output(tmp_path, monkeypatch):
    service = VideoMergeService(str(tmp_path))
    (tmp_path / "clip_720p.mp4").write_text("video")
    (tmp_path / "clip_audio.mp3").write_text("audio")

    def fake_merge(video_path, audio_path, output_file, logger=None):
        Path(output_file).write_text("merged")

    monkeypatch.setattr(
        "pyutube.services.VideoMergeService.ffmpeg_merge_video_audio",
        fake_merge,
    )

    service.merging("clip_720p.mp4", "clip_audio.mp3")

    assert (tmp_path / "clip_720p.mp4").read_text() == "merged"
    assert not (tmp_path / "output").exists()

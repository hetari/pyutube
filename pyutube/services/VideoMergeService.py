"""Merge downloaded video and audio streams."""

import os
import sys

from moviepy.video.io.ffmpeg_tools import ffmpeg_merge_video_audio

from pyutube.ui import error_console


class VideoMergeService:
    """Merge and clean up media files after download."""

    def __init__(self, path: str) -> None:
        self.path = path

    def merging(self, video_name: str, audio_name: str):
        """Merge the downloaded video and audio streams into a single file."""
        output_directory = os.path.join(self.path, "output")
        os.makedirs(output_directory, exist_ok=True)

        base_name = os.path.splitext(os.path.basename(video_name))[0]
        output_file = os.path.join(output_directory, f"{base_name}.mp4")
        video_path = self._find_downloaded_file(video_name)
        audio_path = self._find_downloaded_file(audio_name)

        if video_path is None:
            error_console.print(f"❗ Video file not found: {video_name}")
            sys.exit(1)

        if audio_path is None:
            error_console.print(f"❗ Audio file not found: {audio_name}")
            sys.exit(1)

        try:
            ffmpeg_merge_video_audio(video_path, audio_path, output_file, logger=None)
            os.remove(video_path)
            os.remove(audio_path)

            if os.path.exists(output_file):
                final_path = os.path.join(self.path, os.path.basename(output_file))
                os.replace(output_file, final_path)
                os.rmdir(output_directory)
            else:
                error_console.print("❗ Merged video file not found in the output directory.")
                sys.exit(1)
        except Exception as error:
            error_console.print(f"❗ An error occurred: {error}")
            sys.exit(1)

    def _find_downloaded_file(self, filename: str):
        base_name = os.path.splitext(os.path.basename(filename))[0]
        for file_name in os.listdir(self.path):
            if file_name.startswith(base_name):
                return os.path.join(self.path, file_name)
        return None

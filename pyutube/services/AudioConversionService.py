"""Convert downloaded audio streams into MP3 files."""

import os
import subprocess
import sys

import imageio_ffmpeg

from pyutube.ui import console, error_console


class AudioConversionService:
    """Convert a downloaded audio file to a real MP3 using ffmpeg."""

    def convert_to_mp3(self, input_path: str, output_path: str) -> str:
        """Convert ``input_path`` to ``output_path`` and return the mp3 path."""
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        command = [
            ffmpeg_exe,
            "-y",
            "-i",
            input_path,
            "-vn",
            "-codec:a",
            "libmp3lame",
            "-q:a",
            "2",
            output_path,
        ]

        try:
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError as error:
            error_console.print(f"❗ Error converting audio to mp3: {error}")
            sys.exit(1)

        if os.path.exists(input_path) and input_path != output_path:
            os.remove(input_path)

        console.print("✅ Audio converted to mp3", style="success")
        return output_path

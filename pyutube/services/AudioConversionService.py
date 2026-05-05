"""Convert downloaded audio streams into audio files."""

import os
import subprocess
import sys

import imageio_ffmpeg

from pyutube.ui import console, error_console


class AudioConversionService:
    """Convert a downloaded audio file to a target audio container using ffmpeg."""

    def convert_audio(self, input_path: str, output_path: str) -> str:
        """Convert ``input_path`` to ``output_path`` and return the output path."""
        output_format = os.path.splitext(output_path)[1].lower()
        if output_format == ".mp3":
            ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
            command = [
                ffmpeg_exe,
                "-y",
                "-i",
                input_path,
                "-vn",
                "-c:a",
                "libmp3lame",
                "-q:a",
                "128k",
                output_path,
            ]
            success_message = "✅ Audio converted to mp3"
        else:
            if input_path != output_path:
                os.replace(input_path, output_path)
            console.print("✅ Audio downloaded", style="success")
            return output_path

        try:
            if command and len(command):
                subprocess.run(
                    command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
        except subprocess.CalledProcessError as error:
            error_console.print(
                f"❗ Error converting audio to {output_format.lstrip('.')}: {error}"
            )
            sys.exit(1)

        if os.path.exists(input_path) and input_path != output_path:
            os.remove(input_path)

        console.print(success_message, style="success")
        return output_path

    def convert_to_mp3(self, input_path: str, output_path: str) -> str:
        """Backward-compatible wrapper for MP3 conversion."""
        return self.convert_audio(input_path, output_path)

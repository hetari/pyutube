from typing import Any, Optional
from termcolor import colored
from yaspin import yaspin
from yaspin.spinners import Spinners


class AudioService:
    @staticmethod
    @yaspin(
        text=colored("Downloading the audio...", "green"),
        color="green",
        spinner=Spinners.dots13,
    )
    def get_audio_streams(video: Any) -> Optional[dict]:
        """Return the best available audio-only format."""
        formats = video.get("formats") or []
        audio_formats = [
            fmt
            for fmt in formats
            if fmt.get("acodec") != "none" and fmt.get("vcodec") == "none"
        ]

        if not audio_formats:
            return None

        return max(
            audio_formats,
            key=lambda fmt: (
                fmt.get("abr") or 0,
                fmt.get("tbr") or 0,
                fmt.get("filesize") or fmt.get("filesize_approx") or 0,
            ),
        )

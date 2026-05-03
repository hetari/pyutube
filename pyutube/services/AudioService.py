from pytubefix import YouTube
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
    def get_audio_streams(video: YouTube) -> YouTube:
        """Return the first available audio-only stream."""
        return video.streams.filter(only_audio=True).order_by("mime_type").first()

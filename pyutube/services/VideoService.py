import os
import sys

from moviepy.video.io.ffmpeg_tools import ffmpeg_merge_video_audio
from pytubefix import YouTube
from pytubefix.cli import on_progress
from termcolor import colored
from yaspin import yaspin
from yaspin.spinners import Spinners

from pyutube.utils import CANCEL_PREFIX, ask_resolution, console, error_console


class VideoService:
    def __init__(self, url: str, quality: str, path: str) -> None:
        self.url = url
        self.quality = quality
        self.path = path

    def search_process(self) -> YouTube:
        """Create a ``YouTube`` object for the current URL."""
        try:
            video = self.__video_search()
        except Exception as error:
            error_console.print(f"Error: {error}")
            sys.exit(1)

        if not video:
            error_console.print("No stream available for the url.")
            sys.exit()

        return video

    @yaspin(
        text=colored("Searching for the video", "green"),
        color="green",
        spinner=Spinners.point,
    )
    def __video_search(self) -> YouTube:
        return YouTube(
            self.url,
            use_oauth=True,
            allow_oauth_cache=True,
            on_progress_callback=on_progress,
        )

    @yaspin(text=colored("getting video streams", "green"), spinner=Spinners.point)
    def get_available_resolutions(self, video: YouTube):
        """Return resolution labels, sizes, and the related streams."""
        streams = video.streams
        available_streams = streams.filter(
            progressive=False,
            adaptive=True,
            mime_type="video/mp4",
        )
        audio_stream = streams.filter(only_audio=True).order_by("mime_type").first()
        if audio_stream is None:
            error_console.print("No audio stream was found for this video.")
            sys.exit(1)

        resolutions_with_sizes = self.get_video_resolutions_sizes(
            available_streams,
            audio_stream,
        )
        if not resolutions_with_sizes:
            error_console.print("No downloadable video streams were found.")
            sys.exit(1)

        resolutions_with_sizes = sorted(
            resolutions_with_sizes,
            key=self._resolution_sort_key,
        )

        resolutions, sizes = zip(*resolutions_with_sizes)
        return list(resolutions), list(sizes), available_streams, audio_stream

    @yaspin(text=colored("Downloading the video...", "green"), color="green", spinner=Spinners.dots13)
    def get_video_streams(self, quality: str, streams):
        """Pick the best matching stream for the requested quality."""
        stream = streams.filter(res=quality).first()

        if quality and quality.startswith(CANCEL_PREFIX):
            error_console.print("❗ Cancel the download...")
            sys.exit()

        if stream:
            return stream

        available_qualities = [
            int(resolution.replace("p", ""))
            for resolution in (stream.resolution for stream in streams)
            if resolution and resolution.replace("p", "").isdigit()
        ]
        if not available_qualities:
            error_console.print("❗ No matching video quality was found.")
            sys.exit(1)

        quality_int = int(quality.replace("p", "")) if "p" in quality else int(quality)
        selected_quality = min(
            available_qualities,
            key=lambda value: abs(quality_int - value),
        )
        return streams.filter(res=f"{selected_quality}p").first()

    def get_selected_stream(self, video, is_audio: bool = False):
        """Return the streams needed for the selected download mode."""
        resolutions, sizes, streams, video_audio = self.get_available_resolutions(video)

        if not streams:
            error_console.print("❗ Cancel the download...")
            sys.exit()

        if not is_audio:
            self.quality = self.quality or ask_resolution(resolutions, sizes)
            if not self.quality:
                error_console.print("❗ Cancel the download...")
                sys.exit()

        return streams, video_audio, self.quality

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

    @staticmethod
    def get_video_resolutions_sizes(available_streams, audio_stream):
        """Return resolution labels paired with estimated file sizes."""
        if not available_streams:
            return []

        audio_filesize = audio_stream.filesize
        resolutions_with_sizes = []
        one_mb = 1024 * 1024
        one_gb = one_mb * 1024

        for stream in available_streams:
            if not stream.resolution:
                continue

            video_filesize_bytes = stream.filesize
            if not stream.is_progressive:
                video_filesize_bytes += audio_filesize

            if video_filesize_bytes >= one_gb:
                video_filesize = f"{video_filesize_bytes / one_gb:.4f} GB"
            elif video_filesize_bytes >= one_mb:
                video_filesize = f"{video_filesize_bytes / one_mb:.2f} MB"
            else:
                video_filesize = f"{video_filesize_bytes / 1024:.2f} KB"

            resolutions_with_sizes.append((stream.resolution, video_filesize))

        return resolutions_with_sizes

    @staticmethod
    def _resolution_sort_key(item):
        resolution, _ = item
        numeric_value = resolution[:-1]
        return int(numeric_value) if numeric_value.isdigit() else float("inf")

    def _find_downloaded_file(self, filename: str):
        base_name = os.path.splitext(os.path.basename(filename))[0]
        for file_name in os.listdir(self.path):
            if file_name.startswith(base_name):
                return os.path.join(self.path, file_name)
        return None

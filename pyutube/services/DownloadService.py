import os
import sys

from pytubefix import YouTube
from pytubefix.helpers import safe_filename

from pyutube.handlers.PlaylistHandler import PlaylistHandler
from pyutube.services.FileService import FileService
from pyutube.services.VideoService import VideoService
from pyutube.utils import asking_video_or_audio, console, error_console


class DownloadService:
    def __init__(
        self,
        url: str,
        path: str,
        quality: str,
        is_audio: bool = False,
        make_playlist_in_order: bool = False,
    ):
        self.url = url
        self.path = path
        self.quality = quality
        self.is_audio = is_audio
        self.make_playlist_in_order = make_playlist_in_order

        self.video_service = VideoService(self.url, self.quality, self.path)
        self.file_service = FileService()

    def download(self, title_number: int = 0):
        video, streams, video_audio, self.quality = self.download_preparing()

        if self.is_audio:
            self.download_audio(video, video_audio, title_number)
            return True

        video_file = self.video_service.get_video_streams(self.quality, streams)
        if not video_file:
            error_console.print("Something went wrong while downloading the video.")
            sys.exit()

        return self.download_video(video, video_file, video_audio, title_number)

    def download_audio(
        self,
        video: YouTube,
        video_audio: YouTube,
        title_number: int = 0,
    ) -> str:
        audio_filename = self.file_service.generate_filename(
            video_audio,
            is_audio=True,
        )

        if self.make_playlist_in_order:
            base_name, extension = os.path.splitext(audio_filename)
            audio_filename = f"{title_number}__{base_name}{extension}"

        audio_filename = self.file_service.handle_existing_file(
            video,
            audio_filename,
            self.path,
            self.is_audio,
        )

        try:
            if self.is_audio:
                console.print("⏳ Downloading the audio...", style="info")

            self.file_service.save_file(video_audio, audio_filename, self.path)
        except Exception as error:
            error_console.print(
                f"❗ Error (please report this in github issue: https://github.com/Hetari/pyutube/issues):\n {error}"
            )
            sys.exit()

        if self.is_audio:
            console.print("\n\n✅ Download completed", style="success")

        return audio_filename

    def download_video(
        self,
        video: YouTube,
        video_stream: YouTube,
        video_audio: YouTube,
        title_number: int = 0,
    ):
        video_filename = self.file_service.generate_filename(video_stream)

        if self.make_playlist_in_order:
            video_base_name, video_extension = os.path.splitext(video_filename)
            video_filename = f"{title_number}__{video_base_name}{video_extension}"

        video_filename = self.file_service.handle_existing_file(
            video,
            video_filename,
            self.path,
            self.is_audio,
        )

        try:
            console.print("⏳ Downloading the video...", style="info")
            self.file_service.save_file(video_stream, video_filename, self.path)
            audio_filename = self.download_audio(
                video,
                video_audio,
                title_number,
            )

            video_base_name, video_extension = os.path.splitext(video_filename)
            audio_base_name, audio_extension = os.path.splitext(audio_filename)
            video_safe_filename = f"{safe_filename(video_base_name)}{video_extension}"
            audio_safe_filename = f"{safe_filename(audio_base_name)}{audio_extension}"

            self.video_service.merging(video_safe_filename, audio_safe_filename)
        except Exception as error:
            error_console.print(
                f"❗ Error (please report this in github issue: https://github.com/Hetari/pyutube/issues):\n {error}"
            )
            sys.exit()

        console.print("\n\n✅ Download completed", style="success")
        return self.quality

    def asking_video_or_audio(self):
        choice = asking_video_or_audio()
        if choice is None:
            return

        self.is_audio = choice
        self.download()

    def get_playlist_links(self):
        handler = PlaylistHandler(self.url, self.path)
        result = handler.process_playlist()
        if result is None:
            return

        new_path, is_audio, videos_selected, make_in_order, playlist_videos = result
        self.make_playlist_in_order = make_in_order

        selected_titles = [
            title for title, _video_id in playlist_videos if _video_id in videos_selected
        ]

        for index, video_id in enumerate(videos_selected):
            self.url = f"https://www.youtube.com/watch?v={video_id}"
            self.path = new_path
            self.is_audio = is_audio

            title_number = int(selected_titles[index].split("__")[0]) if make_in_order else 0

            if index == 0:
                self.video_service = VideoService(self.url, self.quality, self.path)
                quality = self.download(title_number)
                continue

            self.quality = quality
            self.video_service = VideoService(self.url, self.quality, self.path)
            self.download(title_number)

    def download_preparing(self):
        video = self.video_service.search_process()
        console.print(f"Title: {video.title}\n", style="info")
        streams, video_audio, self.quality = self.video_service.get_selected_stream(
            video,
            self.is_audio,
        )

        return video, streams, video_audio, self.quality

"""Download every selected item from a playlist."""

from typing import Any, Callable, Optional

from pyutube.handlers.PlaylistHandler import PlaylistHandler
from pyutube.services.SingleDownloadService import SingleDownloadService


class PlaylistDownloadService:
    """Orchestrate playlist selection and sequential downloads."""

    def __init__(
        self,
        single_download_factory: Optional[
            Callable[[str, str, str, bool, str, bool], Any]
        ] = None,
        ytdlp_args: Optional[list[str]] = None,
    ) -> None:
        self.single_download_factory = single_download_factory or self._default_factory
        self.ytdlp_args = list(ytdlp_args or [])

    def _default_factory(
        self,
        url: str,
        path: str,
        quality: str,
        is_audio: bool,
        audio_format: str,
        make_playlist_in_order: bool,
    ):
        return SingleDownloadService(
            url=url,
            path=path,
            quality=quality,
            is_audio=is_audio,
            audio_format=audio_format,
            make_playlist_in_order=make_playlist_in_order,
            ytdlp_args=self.ytdlp_args,
        )

    def download_playlist(self, url: str, path: str, quality: str, audio_format: str) -> None:
        handler = PlaylistHandler(url, path, self.ytdlp_args)
        plan = handler.process_playlist()
        if plan is None:
            return

        new_path = plan.new_path
        is_audio = plan.is_audio
        videos_selected = plan.videos_selected
        make_in_order = plan.make_in_order
        playlist_videos = plan.playlist_videos

        selected_titles = [
            title for title, _video_id in playlist_videos if _video_id in videos_selected
        ]

        for index, video_id in enumerate(videos_selected):
            title_number = (
                int(selected_titles[index].split("__")[0]) if make_in_order else 0
            )
            downloader = self.single_download_factory(
                f"https://www.youtube.com/watch?v={video_id}",
                new_path,
                quality,
                is_audio,
                audio_format,
                make_in_order,
            )

            if index == 0:
                quality = downloader.download(title_number)
                continue

            downloader.quality = quality
            downloader.refresh_video_service()
            downloader.download(title_number)

"""High-level download coordinator for single videos and playlists."""

from typing import Any, Optional

from pyutube.core.prompts import PromptService
from pyutube.services.models import DownloadPreparation, FormatInfo, VideoInfo
from pyutube.services.PlaylistDownloadService import PlaylistDownloadService
from pyutube.services.SingleDownloadService import SingleDownloadService


class DownloadService:
    """Coordinate the download flow while delegating the heavy lifting."""

    def __init__(
        self,
        url: str,
        path: str,
        quality: str = "",
        is_audio: bool = False,
        make_playlist_in_order: bool = False,
        ytdlp_args: Optional[list[str]] = None,
        prompt_service: Optional[PromptService] = None,
    ):
        self.url = url
        self.path = path
        self.quality = quality
        self.is_audio = is_audio
        self.audio_format = "mp3"
        self.make_playlist_in_order = make_playlist_in_order
        self.ytdlp_args = list(ytdlp_args or [])
        self.prompt_service = prompt_service or PromptService()

        self.single_download_service = SingleDownloadService(
            url=self.url,
            path=self.path,
            quality=self.quality,
            is_audio=self.is_audio,
            make_playlist_in_order=self.make_playlist_in_order,
            ytdlp_args=self.ytdlp_args,
        )
        self.playlist_download_service = PlaylistDownloadService(
            self._build_single_download_service,
            self.ytdlp_args,
        )

    @property
    def video_service(self) -> Any:
        return self.single_download_service.video_service

    @property
    def file_service(self) -> Any:
        return self.single_download_service.file_service

    def _build_single_download_service(
        self,
        url: str,
        path: str,
        quality: str,
        is_audio: bool,
        make_playlist_in_order: bool,
    ) -> SingleDownloadService:
        """Create a worker that reuses shared file-conflict and file helpers."""
        return SingleDownloadService(
            url=url,
            path=path,
            quality=quality,
            is_audio=is_audio,
            make_playlist_in_order=make_playlist_in_order,
            ytdlp_args=self.ytdlp_args,
            file_service=self.single_download_service.file_service,
            conflict_resolver=self.single_download_service.conflict_resolver,
        )

    def download(self, title_number: int = 0) -> Any:
        self.single_download_service.is_audio = self.is_audio
        return self.single_download_service.download(title_number)

    def download_audio(
        self,
        video: VideoInfo,
        video_audio: Optional[FormatInfo],
        title_number: int = 0,
    ) -> str:
        return self.single_download_service.download_audio(
            video,
            video_audio,
            title_number,
        )

    def download_video(
        self,
        video: VideoInfo,
        video_stream: FormatInfo,
        title_number: int = 0,
    ) -> str:
        return self.single_download_service.download_video(
            video,
            video_stream,
            title_number,
        )

    def asking_video_or_audio(self) -> None:
        choice = self.prompt_service.asking_video_or_audio()
        if choice is None:
            return

        self.is_audio = choice
        self.single_download_service.is_audio = choice
        self.download()

    def get_playlist_links(self) -> None:
        self.playlist_download_service.download_playlist(
            self.url,
            self.path,
            self.quality,
        )

    def download_preparing(self) -> DownloadPreparation:
        self.single_download_service.is_audio = self.is_audio
        preparation = self.single_download_service.prepare_download()
        self.quality = preparation.quality
        return preparation

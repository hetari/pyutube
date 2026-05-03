"""High-level download coordinator for single videos and playlists."""

from pyutube.services.models import DownloadPreparation
from pyutube.services.PlaylistDownloadService import PlaylistDownloadService
from pyutube.services.SingleDownloadService import SingleDownloadService
from pyutube.utils import asking_video_or_audio


class DownloadService:
    """Coordinate the download flow while delegating the heavy lifting."""

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

        self.single_download_service = SingleDownloadService(
            url=self.url,
            path=self.path,
            quality=self.quality,
            is_audio=self.is_audio,
            make_playlist_in_order=self.make_playlist_in_order,
        )
        self.playlist_download_service = PlaylistDownloadService(
            self._build_single_download_service
        )

        self._sync_services()

    def _sync_services(self) -> None:
        """Keep the coordinator and the single-download worker aligned."""
        self.single_download_service.url = self.url
        self.single_download_service.path = self.path
        self.single_download_service.quality = self.quality
        self.single_download_service.is_audio = self.is_audio
        self.single_download_service.make_playlist_in_order = (
            self.make_playlist_in_order
        )
        self.single_download_service.refresh_video_service()
        self.video_service = self.single_download_service.video_service
        self.file_service = self.single_download_service.file_service

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
            file_service=self.file_service,
            conflict_resolver=self.single_download_service.conflict_resolver,
        )

    def download(self, title_number: int = 0):
        self._sync_services()
        return self.single_download_service.download(title_number)

    def download_audio(
        self,
        video,
        video_audio,
        title_number: int = 0,
    ):
        self._sync_services()
        return self.single_download_service.download_audio(
            video,
            video_audio,
            title_number,
        )

    def download_video(
        self,
        video,
        video_stream,
        video_audio,
        title_number: int = 0,
    ):
        self._sync_services()
        return self.single_download_service.download_video(
            video,
            video_stream,
            video_audio,
            title_number,
        )

    def asking_video_or_audio(self):
        choice = asking_video_or_audio()
        if choice is None:
            return

        self.is_audio = choice
        self.download()

    def get_playlist_links(self):
        self._sync_services()
        self.playlist_download_service.download_playlist(
            self.url,
            self.path,
            self.quality,
        )

    def download_preparing(self) -> DownloadPreparation:
        self._sync_services()
        preparation = (
            self.single_download_service.prepare_download()
        )
        self.quality = preparation.quality
        return preparation

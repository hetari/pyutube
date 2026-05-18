"""
Pyutube is a command-line interface, a versatile tool
to download YouTube videos, shorts, and playlists.

This module provides a command-line interface (CLI), a powerful tool designed
to simplify the process of downloading YouTube content directly from the terminal.
Pyutube supports downloading videos (as video or audio), shorts, and playlists,
offering users flexibility and convenience in managing their media downloads.

Usage:
    $ pyutube <URL> [options]
    $ pyutube <URL> [options] -- <yt-dlp options>

Options:
    -a, --audio          Download only audio.
    --mp3                Convert audio downloads to MP3.
    -f, --footage        Download only video (footage).
    -v, --version        Show the version number.

Example:
    $ pyutube <YouTube_URL> -a
        Download the audio of the specified YouTube video as WAV.

    $ pyutube <YouTube_URL> -a --mp3
        Download the audio of the specified YouTube video as MP3.

    $ pyutube <YouTube_URL> -f
        Download the video (footage) of the specified YouTube video.

    $ pyutube <YouTube_URL>
        Download the file of the specified YouTube video,
        it will ask you about downloading it as video or audio.

    $ pyutube <YouTube_playlist_URL>
        Download all videos from the specified YouTube playlist.

    $ pyutube <YouTube_short_URL>
        Download the specified YouTube short video.

    $ pyutube <YouTube_URL> -- --ignore-errors --write-info-json
        Forward extra yt-dlp options directly to yt-dlp.

        Pyutube still manages the URL, save path, and interactive format
        selection, so output-related flags may be overridden by the app.

Made with ❤️ By Ebraheem. Find me on GitHub: @Hetari. The project lives on @Hetari/pyutube.

Thank you for using Pyutube! Your support is greatly appreciated. ⭐️
"""

import os
import sys

import typer

from pyutube.handlers import URLHandler
from pyutube.services.DownloadService import DownloadService
from pyutube.utils import (
    __version__,
    check_for_updates,
    check_internet_connection,
    clear,
    console,
    error_console,
)

app = typer.Typer(
    name="pyutube",
    add_completion=False,
    help="Download YouTube videos, audio, shorts, and playlists from the terminal.",
    rich_markup_mode="rich",
    context_settings={
        "allow_extra_args": True,
        "ignore_unknown_options": True,
    },
)


url_arg = typer.Argument(None, help="YouTube URL [red]required[/red]", show_default=False)
path_arg = typer.Argument(
    os.getcwd(), help="Path to save video [cyan]default: <current directory>[/cyan]", show_default=False
)
audio_option = typer.Option(False, "-a", "--audio", help="Download only audio")
mp3_option = typer.Option(False, "--mp3", help="Convert audio downloads to MP3")
video_option = typer.Option(False, "-f", "--footage", help="Download only video")
version_option = typer.Option(False, "-v", "--version", help="Show the version number")


@app.command(
    name="download",
    help="Download YouTube videos, audio, shorts, and playlists.",
    epilog=(
        "Made with ❤️ By Ebraheem. Find me on GitHub: "
        "[link=https://github.com/Hetari]@Hetari[/link].\n\n"
        "The project lives on [link=https://github.com/Hetari/pyutube]@Hetari/pyutube[/link]."
    ),
)
def pyutube(
    ctx: typer.Context,
    url: str = url_arg,
    path: str = path_arg,
    audio: bool = audio_option,
    mp3: bool = mp3_option,
    video: bool = video_option,
    version: bool = version_option,
) -> None:
    if version:
        console.print(f"Pyutube {__version__}")
        sys.exit()

    check_for_updates()

    if url is None:
        error_console.print("❗ Missing argument 'URL'.")
        sys.exit()

    clear()

    if not check_internet_connection():
        sys.exit()

    url_handler = URLHandler(url)
    is_valid_link, link_type = url_handler.validate()

    if not is_valid_link:
        sys.exit()

    audio_format = "mp3" if mp3 else "wav"
    yt_dlp_args = list(ctx.args)
    download_service = DownloadService(
        url,
        path,
        "",
        audio_format=audio_format,
        ytdlp_args=yt_dlp_args,
    )
    if audio:
        download_service.is_audio = True
        preparation = download_service.download_preparing()
        download_service.download_audio(preparation.video, preparation.video_audio)

    elif video or link_type == "short":
        preparation = download_service.download_preparing()
        video_file = download_service.video_service.get_video_streams(
            preparation.quality,
            preparation.streams,
        )
        download_service.download_video(
            preparation.video,
            video_file,
        )

    elif link_type == "video":
        download_service.asking_video_or_audio()

    elif link_type == "playlist":
        download_service.get_playlist_links()

    else:
        error_console.print("❗ Unsupported link type.")
        sys.exit()

    sys.exit()

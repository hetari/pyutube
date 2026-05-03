"""Utility helpers for the pyutube package."""

import os
import subprocess
import sys
from typing import Any, Optional

import inquirer
import requests
from pytubefix import __version__ as pytubefix_version
from rich.console import Console
from rich.theme import Theme
from termcolor import colored
from yaspin import yaspin
from yaspin.spinners import Spinners

__version__ = "1.5.0"
__app__ = "pyutube"
ABORTED_PREFIX = "Aborted"
CANCEL_PREFIX = "Cancel"

custom_theme = Theme(
    {
        "info": "#64b0f2",
        "warning": "color(3)",
        "success": "green",
    }
)
console = Console(theme=custom_theme)
error_console = Console(stderr=True, style="red")


def clear() -> None:
    """Clear the terminal screen on the current platform."""
    os.system("cls" if os.name == "nt" else "clear")


@yaspin(text="Checking internet connection", color="blue", spinner=Spinners.earth)
def is_internet_available() -> bool:
    """Return ``True`` when a basic outbound request succeeds."""
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.RequestException:
        return False


def _prompt_choice(question: Any) -> Optional[Any]:
    """Return the selected value for a single inquirer question."""
    try:
        response = inquirer.prompt([question])
    except Exception as error:
        error_console.print(f"Error: {error}")
        sys.exit(1)

    if not response:
        return None

    return response.get(question.name)


def file_type() -> Optional[str]:
    """Ask whether the user wants audio or video output."""
    question = inquirer.List(
        "file_type",
        message="Choose the file type you want to download",
        choices=["Audio", "Video", CANCEL_PREFIX],
    )
    choice = _prompt_choice(question)
    return choice


def ask_resolution(resolutions, sizes) -> Optional[str]:
    """Ask the user to choose a video resolution."""
    size_resolution_mapping = dict(zip(resolutions, sizes))
    choices = [
        f"{size} ~= {resolution}"
        for size, resolution in size_resolution_mapping.items()
    ] + [CANCEL_PREFIX]

    question = inquirer.List(
        "resolution",
        message="Choose the resolution you want to download",
        choices=choices,
    )
    choice = _prompt_choice(question)
    if choice is None:
        return None

    return choice.split(" ~= ")[0]


def ask_rename_file(filename: str) -> Optional[str]:
    """Ask the user how to handle a filename conflict."""
    console.print(f"'{filename}' already exists. What do you want to do?", style="info")

    question = inquirer.List(
        "rename",
        message="Choose an action",
        choices=["Rename it", "Overwrite it", CANCEL_PREFIX],
    )
    return _prompt_choice(question)


def ask_playlist_video_names(videos) -> Optional[list]:
    """Ask which playlist videos should be downloaded."""
    note = colored("NOTE:", "cyan")
    select_one = colored("<space>", "red")
    select_all = colored("<ctrl+a>", "red")
    invert_selection = colored("<ctrl+i>", "red")
    restart_selection = colored("<ctrl+r>", "red")

    print(
        f"{note} Press {select_one} to select the videos, {select_all} to select all, "
        f"{invert_selection} to invert selection, and {restart_selection} to restart selection"
    )

    question = inquirer.Checkbox(
        "names",
        message="Choose the videos you want to download",
        choices=videos,
    )
    return _prompt_choice(question)


def ask_for_make_playlist_in_order() -> Optional[bool]:
    """Ask whether playlist items should be prefixed with their order number."""
    question = inquirer.Confirm(
        "ask_for_make_playlist_in_order",
        message="Do you want to add the number order of the videos (ex: 1, 2, ...etc)?",
        default=False,
    )
    return _prompt_choice(question)


def check_for_updates() -> None:
    """Check PyPI for newer versions of the main dependencies."""
    libraries = {
        "pyutube": {
            "version": __version__,
        },
        "pytubefix": {
            "version": pytubefix_version,
        },
    }

    try:
        for library, metadata in libraries.items():
            response = requests.get(
                f"https://pypi.org/pypi/{library}/json",
                headers={"Accept": "application/json"},
                timeout=10,
            )
            if response.status_code != 200:
                error_console.print(
                    f"❗ Error checking for updates: {response.status_code}"
                )
                continue

            latest_version = response.json()["info"]["version"]
            if latest_version == metadata["version"]:
                continue

            console.print(
                f"👉 A new version of [blue]{library}[/blue] is available: {latest_version}. "
                f"Updating it now...",
                style="warning",
            )

            try:
                subprocess.check_call(
                    [
                        sys.executable,
                        "-m",
                        "pip",
                        "install",
                        "--upgrade",
                        library,
                        "--break-system-packages",
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                console.print(
                    f"✅ Successfully updated [blue]{library}[/blue] to version {latest_version}.",
                    style="success",
                )
            except subprocess.CalledProcessError as error:
                error_console.print(
                    f"❗ Failed to update [blue]{library}[/blue]: {error.stderr.decode()}"
                )
                console.print(
                    f"❗ Update {library} manually with: pip install --upgrade {library}",
                    style="warning",
                )
    except Exception as error:
        error_console.print(f"❗ Error checking for updates: {error}")


def check_internet_connection() -> bool:
    """Return ``True`` only when an internet connection is available."""
    if not is_internet_available():
        error_console.print("❗ No internet connection")
        return False

    console.print("✅ There is internet connection", style="success")
    console.print()
    return True


def asking_video_or_audio() -> Optional[bool]:
    """Return ``True`` for audio downloads and ``False`` for video downloads."""
    choice = file_type()
    if choice is None or choice.startswith(CANCEL_PREFIX):
        return None

    return choice.lower().startswith("audio")

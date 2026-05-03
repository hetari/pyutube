"""Prompt helpers used by the CLI and download workflows."""

import sys
from typing import Any, Optional

import inquirer
from termcolor import colored

from pyutube.ui import console


class PromptService:
    """Collect user input through a narrow, testable interface."""

    cancel_prefix = "Cancel"

    @staticmethod
    def _prompt_choice(question: Any) -> Optional[Any]:
        try:
            response = inquirer.prompt([question])
        except Exception as error:
            console.print(f"Error: {error}")
            sys.exit(1)

        if not response:
            return None

        return response.get(question.name)

    def file_type(self) -> Optional[str]:
        question = inquirer.List(
            "file_type",
            message="Choose the file type you want to download",
            choices=["Audio", "Video", self.cancel_prefix],
        )
        return self._prompt_choice(question)

    def ask_resolution(self, resolutions, sizes) -> Optional[str]:
        size_resolution_mapping = dict(zip(resolutions, sizes))
        choices = [
            f"{size} ~= {resolution}"
            for size, resolution in size_resolution_mapping.items()
        ] + [self.cancel_prefix]

        question = inquirer.List(
            "resolution",
            message="Choose the resolution you want to download",
            choices=choices,
        )
        choice = self._prompt_choice(question)
        if choice is None:
            return None

        return choice.split(" ~= ")[0]

    def ask_rename_file(self, filename: str) -> Optional[str]:
        console.print(f"'{filename}' already exists. What do you want to do?", style="info")

        question = inquirer.List(
            "rename",
            message="Choose an action",
            choices=["Rename it", "Overwrite it", self.cancel_prefix],
        )
        return self._prompt_choice(question)

    def ask_playlist_video_names(self, videos) -> Optional[list]:
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
        return self._prompt_choice(question)

    def ask_for_make_playlist_in_order(self) -> Optional[bool]:
        question = inquirer.Confirm(
            "ask_for_make_playlist_in_order",
            message="Do you want to add the number order of the videos (ex: 1, 2, ...etc)?",
            default=False,
        )
        return self._prompt_choice(question)

    def asking_video_or_audio(self) -> Optional[bool]:
        choice = self.file_type()
        if choice is None or choice.startswith(self.cancel_prefix):
            return None

        return choice.lower().startswith("audio")

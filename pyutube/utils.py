"""Utility helpers and constants for the pyutube package."""

import os
import re

__app__ = "pyutube"
ABORTED_PREFIX = "Aborted"
CANCEL_PREFIX = "Cancel"


def clear() -> None:
    """Clear the terminal screen on the current platform."""
    os.system("cls" if os.name == "nt" else "clear")


def safe_filename(value: str) -> str:
    """Return a filesystem-safe filename fragment."""
    cleaned = re.sub(r'[\\/:*?"<>|\x00-\x1f]+', "_", value)
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" ._")
    return cleaned or "download"

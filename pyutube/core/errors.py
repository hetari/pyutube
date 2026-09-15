"""Compatibility module for errors — canonical logic lives in pyutube.core.exceptions."""

from pyutube.core.exceptions import (
    DownloadCancelledError,
    InvalidInputError,
    NoStreamAvailableError,
    NoVideoFoundError,
    PyutubeError,
    _log_directory,
    handle_error,
)

__all__ = [
    "DownloadCancelledError",
    "InvalidInputError",
    "NoStreamAvailableError",
    "NoVideoFoundError",
    "PyutubeError",
    "_log_directory",
    "handle_error",
]

"""Custom exceptions and centralized error reporting for pyutube."""

import platform
import sys
import tempfile
import traceback
from pathlib import Path
from typing import Optional

from pyutube.core.logger import logger
from pyutube.ui import error_console
from pyutube.version import __version__


class PyutubeError(Exception):
    """Base exception for all pyutube errors."""

    def __init__(self, message: str = "An error occurred in pyutube.", exit_code: int = 1):
        super().__init__(message)
        self.message = message
        self.exit_code = exit_code


class DownloadCancelledError(PyutubeError):
    """User cancelled the download."""

    def __init__(self, message: str = "Download cancelled by user.", exit_code: int = 0):
        super().__init__(message, exit_code=exit_code)


class NoStreamAvailableError(PyutubeError):
    """No matching stream was found."""

    def __init__(self, message: str = "No downloadable stream found matching criteria.", exit_code: int = 1):
        super().__init__(message, exit_code=exit_code)


class NoVideoFoundError(PyutubeError):
    """No video metadata could be retrieved for the URL."""

    def __init__(self, message: str = "No video found for the provided URL.", exit_code: int = 1):
        super().__init__(message, exit_code=exit_code)


class InvalidInputError(PyutubeError):
    """User-provided input is invalid."""

    def __init__(self, message: str = "Invalid input provided.", exit_code: int = 1):
        super().__init__(message, exit_code=exit_code)


def _log_directory() -> Path:
    """Return a writable directory for error logs."""
    candidates = [
        Path.home() / ".pyutube" / "logs",
        Path(tempfile.gettempdir()) / "pyutube",
    ]
    for candidate in candidates:
        try:
            candidate.mkdir(parents=True, exist_ok=True)
            return candidate
        except OSError:
            continue
    return Path(".")


def handle_error(error: Exception, context: Optional[str] = None) -> None:
    """Format and print a detailed error report for troubleshooting and GitHub issues."""
    try:
        import yt_dlp

        ytdlp_ver = getattr(yt_dlp, "__version__", "unknown")
    except Exception:
        ytdlp_ver = "unknown"

    exc_type = type(error).__name__
    exc_msg = str(error) or "No error message provided."
    tb_str = traceback.format_exc()
    if not tb_str or tb_str.strip() == "NoneType: None":
        tb_str = "".join(
            traceback.format_exception(type(error), error, error.__traceback__)
        )

    pyutube_ver = __version__
    python_ver = sys.version.split()[0]
    os_info = platform.platform()

    error_console.print(
        "\n[bold red]──────────────────────────────────────── Error Report ────────────────────────────────────────[/bold red]"
    )
    error_console.print("❗ [bold red]An unexpected error occurred![/bold red]")
    if context:
        error_console.print(f"📌 [bold yellow]Context:[/bold yellow] {context}")

    error_console.print("\n📌 [bold cyan]Environment Details:[/bold cyan]")
    error_console.print(f"   • Pyutube Version: [green]{pyutube_ver}[/green]")
    error_console.print(f"   • yt-dlp Version:  [green]{ytdlp_ver}[/green]")
    error_console.print(f"   • Python Version:  [green]{python_ver}[/green]")
    error_console.print(f"   • OS / Platform:   [green]{os_info}[/green]")

    error_console.print("\n📌 [bold cyan]Error Details:[/bold cyan]")
    error_console.print(f"   • Exception Type:    [yellow]{exc_type}[/yellow]")
    error_console.print(f"   • Exception Message: [red]{exc_msg}[/red]")

    trace_steps = logger.get_trace()
    if trace_steps:
        error_console.print("\n📌 [bold cyan]Execution Flow Log:[/bold cyan]")
        for idx, step in enumerate(trace_steps, 1):
            error_console.print(f"   {idx:2d}. {step}")

    if tb_str and tb_str.strip() and tb_str.strip() != "NoneType: None":
        error_console.print("\n📌 [bold cyan]Traceback:[/bold cyan]")
        error_console.print(f"[dim]{tb_str.strip()}[/dim]")

    log_file_path = str(_log_directory() / "pyutube_error.log")
    log_path = logger.save_log_file(
        log_file_path,
        error_info=f"Context: {context}\nType: {exc_type}\nMessage: {exc_msg}\n\nTraceback:\n{tb_str}",
    )
    error_console.print(f"\n📄 [bold cyan]Execution Log Saved To:[/bold cyan] {log_path}")

    network_keywords = [
        "network",
        "connection",
        "unreachable",
        "address family",
        "timed out",
        "downloaderror",
        "http",
        "url",
        "dns",
        "socket",
        "101",
        "-9",
    ]
    err_lower = f"{exc_type} {exc_msg}".lower()
    if any(kw in err_lower for kw in network_keywords):
        error_console.print(
            "\n💡 [bold yellow]Hint:[/bold yellow] If you are experiencing connection or network issues, try opening a VPN and trying again. If the issue happens again while the VPN is open, please report the bug."
        )

    error_console.print(
        "\n[bold yellow]Please report this in a GitHub issue:[/bold yellow] "
        "[link=https://github.com/Hetari/pyutube/issues]https://github.com/Hetari/pyutube/issues[/link]"
    )
    error_console.print(
        "Include the full error report above so we can help fix it quickly!"
    )
    error_console.print(
        "[bold red]─────────────────────────────────────────────────────────────────────────────────────────────[/bold red]\n"
    )

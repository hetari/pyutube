"""Centralized error handling and reporting for pyutube."""

import platform
import sys
import traceback
from typing import Optional

from pyutube.ui import error_console
from pyutube.version import __version__


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

    if tb_str and tb_str.strip() and tb_str.strip() != "NoneType: None":
        error_console.print("\n📌 [bold cyan]Traceback:[/bold cyan]")
        error_console.print(f"[dim]{tb_str.strip()}[/dim]")

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

"""Shared terminal output objects for pyutube."""

from rich.console import Console
from rich.theme import Theme


custom_theme = Theme(
    {
        "info": "#64b0f2",
        "warning": "color(3)",
        "success": "green",
    }
)
console = Console(theme=custom_theme)
error_console = Console(stderr=True, style="red")

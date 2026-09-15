"""Package update checks."""

import re
from dataclasses import dataclass
from typing import Dict, Optional

import requests
from yt_dlp.version import __version__ as yt_dlp_version

from pyutube.ui import console, error_console
from pyutube.version import __version__


@dataclass(frozen=True)
class PackageVersion:
    """Version metadata for a package."""

    name: str
    version: str


class UpdateChecker:
    """Check PyPI for newer versions of pyutube dependencies."""

    def __init__(self) -> None:
        self.packages: Dict[str, PackageVersion] = {
            "pyutube": PackageVersion("pyutube", __version__),
            "yt-dlp": PackageVersion("yt-dlp", yt_dlp_version),
        }

    @staticmethod
    def _version_key(version: str) -> tuple[int, ...]:
        """Return a sortable version key for simple dot-separated versions."""
        parts = [part for part in re.split(r"\D+", version) if part]
        return tuple(int(part) for part in parts)

    def _should_upgrade(self, latest_version: str, current_version: str) -> bool:
        """Return True only when the latest version is newer than the current one."""
        return self._version_key(latest_version) > self._version_key(current_version)

    def _fetch_latest_version(self, package_name: str) -> Optional[str]:
        response = requests.get(
            f"https://pypi.org/pypi/{package_name}/json",
            headers={"Accept": "application/json"},
            timeout=10,
        )
        if response.status_code != 200:
            error_console.print(
                f"❗ Error checking for updates: {response.status_code}"
            )
            return None

        return response.json()["info"]["version"]

    def check_for_updates(self) -> None:
        try:
            for package_name, metadata in self.packages.items():
                latest_version = self._fetch_latest_version(package_name)
                if (
                    latest_version is None
                    or latest_version == metadata.version
                    or not self._should_upgrade(latest_version, metadata.version)
                ):
                    continue

                console.print(
                    f"👉 A new version of [blue]{package_name}[/blue] is available: {latest_version}. "
                    f"Update with: pip install --upgrade {package_name}",
                    style="warning",
                )
        except Exception as error:
            error_console.print(f"❗ Error checking for updates: {error}")

"""Package update checks."""

import re
import subprocess
import sys
from dataclasses import dataclass
from importlib import import_module
from typing import Dict, Optional

from yt_dlp.version import __version__ as yt_dlp_version

from pyutube.ui import console, error_console
from pyutube.version import __version__

requests = import_module("requests")


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

    def _upgrade_package(self, package_name: str, latest_version: str) -> None:
        try:
            subprocess.check_call(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "--upgrade",
                    package_name,
                    "--break-system-packages",
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            console.print(
                f"✅ Successfully updated [blue]{package_name}[/blue] to version {latest_version}.",
                style="success",
            )
        except subprocess.CalledProcessError as error:
            error_console.print(
                f"❗ Failed to update [blue]{package_name}[/blue]: {error.stderr.decode()}"
            )
            console.print(
                f"❗ Update {package_name} manually with: pip install --upgrade {package_name}",
                style="warning",
            )

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
                    "Updating it now...",
                    style="warning",
                )
                self._upgrade_package(package_name, latest_version)
        except Exception as error:
            error_console.print(f"❗ Error checking for updates: {error}")

"""Package update checks."""

import subprocess
import sys
from dataclasses import dataclass
from typing import Dict

import requests
from pytubefix import __version__ as pytubefix_version

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
            "pytubefix": PackageVersion("pytubefix", pytubefix_version),
        }

    def _fetch_latest_version(self, package_name: str) -> str | None:
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
                if latest_version is None or latest_version == metadata.version:
                    continue

                console.print(
                    f"👉 A new version of [blue]{package_name}[/blue] is available: {latest_version}. "
                    "Updating it now...",
                    style="warning",
                )
                self._upgrade_package(package_name, latest_version)
        except Exception as error:
            error_console.print(f"❗ Error checking for updates: {error}")

"""Network checks for pyutube."""

import requests  # type: ignore[import-untyped]
from yaspin import yaspin
from yaspin.spinners import Spinners

from pyutube.ui import console, error_console


class InternetChecker:
    """Check whether a basic outbound request succeeds."""

    @staticmethod
    @yaspin(text="Checking internet connection", color="blue", spinner=Spinners.earth)
    def is_available() -> bool:
        try:
            requests.get("https://www.google.com", timeout=5)
            return True
        except requests.RequestException:
            return False

    def check(self) -> bool:
        if not self.is_available():
            error_console.print("❗ No internet connection")
            return False

        console.print("✅ There is internet connection", style="success")
        console.print()
        return True


def is_internet_available() -> bool:
    return InternetChecker.is_available()


def check_internet_connection() -> bool:
    return InternetChecker().check()

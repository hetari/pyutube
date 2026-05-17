"""Setup configuration for the pyutube package."""

from pathlib import Path

from setuptools import find_packages, setup


def read_version() -> str:
    """Read the package version without importing runtime dependencies."""
    namespace: dict[str, str] = {}
    version_file = Path(__file__).parent / "pyutube" / "version.py"
    exec(version_file.read_text(encoding="utf-8"), namespace)
    return namespace["__version__"]


with open("README.md", "r", encoding="utf-8") as f:
    description = f.read()

# Setup configuration
setup(
    name="pyutube",

    version=read_version(),

    author="Ebraheem Alhetari",

    author_email="hetari4all@gmail.com",

    description="Awesome CLI to download YouTube videos (as video or audio)/shorts/playlists from the terminal",

    long_description=description,

    long_description_content_type="text/markdown",

    keywords=[
        "youtube",
        "download",
        "cli",
        "pyutube",
        "pytubefix",
        "pytube",
        "youtube-dl",
    ],

    license="MIT",

    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],

    include_package_data=True,

    python_requires=">=3.6",

    install_requires=[
        "pytubefix",
        "inquirer",
        "yaspin",
        "typer",
        "requests",
        "rich",
        "termcolor",
        "moviepy",
        "setuptools",
        "imageio-ffmpeg",
    ],

    extras_require={
        "dev": [
            "mypy>=1.8,<2.0",
            "types-requests>=2.32.0,<3.0",
            "ruff>=0.9,<1.0",
        ],
    },

    entry_points={
        "console_scripts": [
            "pyutube=pyutube.cli:app",
        ],
    },

    project_urls={
        "Author": "https://github.com/Hetari",
        "Homepage": "https://github.com/Hetari/pyutube",
        "Bug Tracker": "https://github.com/Hetari/pyutube/issues",
        "Source Code": "https://github.com/Hetari/pyutube",
        "Documentation": "https://github.com/Hetari/pyutube",
    },

    platforms=["Linux", "Windows", "MacOS"],
    packages=find_packages()
)

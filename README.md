# 📹 Pyutube - The Simplest YouTube Downloader CLI

### Enjoying my project? Please show your appreciation by starring it on GitHub! ⭐

<a href="https://deepwiki.com/Hetari/pyutube">
    <img src="https://deepwiki.com/badge.svg" alt="Ask in DeepWiki" />
</a>
<a href="https://github.com/Hetari/pyutube">
  <img src="https://img.shields.io/pypi/v/pyutube.svg?style=flat&label=Version" alt="Version">
</a>
<a href="https://pepy.tech/projects/pyutube">
  <img src="https://static.pepy.tech/badge/pyutube" alt="Downloads">
</a>
<a href="https://pepy.tech/projects/pyutube">
  <img src="https://static.pepy.tech/badge/pyutube/month" alt="Downloads per Month">
</a>
<a href="https://pepy.tech/projects/pyutube">
  <img src="https://static.pepy.tech/badge/pyutube/week" alt="Downloads per Week">
</a>

Pyutube is a small CLI for downloading YouTube videos, shorts, audio, and playlists.

<a href="https://ibb.co/27wcFYN">
   <img src="https://i.ibb.co/MDbPg56/Screenshot-from-2024-04-08-21-38-02-transformed.png" alt="Pyutube" style="width: 100%;">
</a>

> [!NOTE]
> Have a feature request or bug report? [tell me](https://github.com/Hetari/pyutube/issues/new)

## Install

```bash
pip install pyutube
```

For local development:

```bash
pip install -e ".[dev]"
```

## Use

```bash
pyutube "<youtube-url>"
pyutube "<youtube-url>" "/path/to/save"
pyutube "<youtube-url>" -a
pyutube "<youtube-url>" -f
pyutube "<playlist-url>"
pyutube "<youtube-url>" -- --ignore-errors --write-info-json
```

Short version:

- `URL` is required.
- `PATH` is optional and defaults to the current directory.
- `-a` downloads audio only (as MP3).
- `-f` downloads video only.
- Playlist URLs first show a selection menu so you can choose specific items or download all.
- Anything after `--` is forwarded to `yt-dlp`.

Check the CLI help:

```bash
pyutube --help
python -m pyutube --help
```

## Docs

- [EXAMPLES.md](EXAMPLES.md) for quick command examples.
- [QUALITY.md](QUALITY.md) for local checks.
- [CONTRIBUTING.md](CONTRIBUTING.md) for contribution rules.

## License

MIT. See [LICENSE](LICENSE).

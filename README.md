# Pyutube

Pyutube is a small CLI for downloading YouTube videos, shorts, audio, and playlists.

> [!IMPORTANT]
> `ffmpeg` must be on your `PATH` for video merging and audio conversion.

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
pyutube "<youtube-url>" -a --mp3
pyutube "<youtube-url>" -f
pyutube "<playlist-url>"
pyutube "<youtube-url>" -- --ignore-errors --write-info-json
```

Short version:

- `URL` is required.
- `PATH` is optional and defaults to the current directory.
- `-a` downloads audio only.
- `--mp3` converts audio output to MP3.
- `-f` downloads video only.
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

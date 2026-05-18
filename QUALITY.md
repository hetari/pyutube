# Quality

Use these checks before opening a pull request:

```bash
python -m compileall pyutube
ruff check pyutube
mypy pyutube
```

## Manual Checks

- `pyutube "<youtube-url>"` downloads a video.
- `pyutube "<youtube-url>" -a` downloads audio.
- `pyutube "<playlist-url>"` handles playlists.
- `ffmpeg` is available on `PATH`.
- Imports do not create circular dependencies.

## What We Expect

- Small, focused modules.
- Clear names for functions and files.
- No syntax errors or packaging mismatches.

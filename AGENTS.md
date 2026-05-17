# Repository Guidelines

## Project Structure & Module Organization
- `pyutube/` contains the package code.
- `pyutube/cli.py` defines the Typer CLI entry point, `pyutube/utils.py` holds shared helpers, and `pyutube/services/` and `pyutube/handlers/` contain download and URL/playlist logic.
- `images/` stores screenshots and README assets.
- Top-level packaging and release files include `setup.py`, `requirements.txt`, `build.sh`, `package.json`, and `MANIFEST.in`.

## Build and Development Commands
- `python3 setup.py sdist bdist_wheel` builds source and wheel distributions.
- `./build.sh` removes old build artifacts, rebuilds packages, and cleans generated caches.
- `python -m pyutube --help` or `pyutube --help` runs the CLI locally.
- `pip install -r requirements.txt` installs the pinned runtime dependencies.

## Coding Style & Naming Conventions
- Use Python 3 style with 4-space indentation and explicit, readable function names.
- Prefer `snake_case` for functions and variables; keep module names aligned with their purpose, such as `DownloadService.py` and `URLHandler.py`.
- Keep functions small and practical. The existing codebase favors functions over deep class hierarchies.
- Match the current import style: standard library first, then third-party, then local imports.

## Commit & Pull Request Guidelines
- Recent commits use short prefixes such as `fix:`, `chore:`, and version-tag commits like `1.5.0`.
- Keep commit messages concise and imperative, e.g. `fix: handle empty playlist names`.
- PRs should include a short summary and any user-visible impact.
- For behavior changes, link the related issue and include screenshots only when CLI output or documentation images change.

## Configuration & Release Notes
- Dependencies are pinned in `requirements.txt`; update them deliberately.
- `build.sh` uses `pip uninstall pyutube -y --break-system-packages`, so review environment impact before running it on a shared machine.

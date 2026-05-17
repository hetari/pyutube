# Code Health

Use these checks to judge whether the repository is healthy:

## Baseline

```bash
python -m compileall pyutube
```

## Static Checks

```bash
ruff check pyutube
mypy pyutube
```

## What Good Looks Like

- No import cycles.
- No syntax errors or packaging mismatches.
- Named dataclasses are used instead of unpacked tuples for flow state.
- Each module has one clear responsibility.
- Code is clean, documented, and easy to read.

## Repo-Specific Checks

- CLI run locally works correctly for downloading single video, short, and playlists.
- Package imports do not trigger circular imports.

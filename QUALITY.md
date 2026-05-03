# Code Health

Use these checks to judge whether the repository is healthy:

## Baseline

```bash
python -m compileall pyutube
pytest pyutube/tests -q
```

## Static Checks

```bash
ruff check pyutube
mypy pyutube
```

## Coverage

```bash
coverage run -m pytest pyutube/tests -q
coverage report
```

## What Good Looks Like

- Tests pass without skipping core flows.
- No import cycles.
- No syntax errors or packaging mismatches.
- Named dataclasses are used instead of unpacked tuples for flow state.
- Each module has one clear responsibility.
- CLI behavior is covered by smoke tests or integration tests.

## Repo-Specific Checks

- URL parsing and URL validation remain covered.
- Single-download and playlist download flows are covered with mocks.
- File conflict behavior is covered.
- Video merge cleanup is covered.
- Package imports do not trigger circular imports.

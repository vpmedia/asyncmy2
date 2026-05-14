# AGENTS.md

## Overview

A fast asyncio MySQL/MariaDB driver. API-compatible with `aiomysql`, with the core protocol rewritten in Cython for speed; supports MySQL replication protocol over asyncio. Community-maintained fork of `long2ice/asyncmy`.

## Tech Stack

- **Language:** Python (>=3.10), Cython
- **Build:** PDM backend (`pdm-backend`), `setuptools`, `wheel`, custom `build.py`, `cibuildwheel`
- **Package Manager:** uv
- **Testing:** pytest, pytest-asyncio, pytest-mock, pytest-xdist, aiomysql, pymysql, mysqlclient, uvloop (non-Windows)
- **Lint/Format:** ruff
- **Type Checking:** mypy, pyright
- **Tooling:** Make, lefthook (git hooks), commitlint

## Documentation

- Cython: https://context7.com/cython/cython/llms.txt
- Lefthook: https://lefthook.dev/llms.txt
- mypy: https://mypy.readthedocs.io/en/stable/llms.txt
- pytest: https://docs.pytest.org/en/stable/llms.txt
- pytest-asyncio: https://context7.com/pytest-dev/pytest-asyncio/llms.txt
- Ruff: https://docs.astral.sh/ruff/llms.txt
- uv: https://docs.astral.sh/uv/llms.txt

## Commands

- **Install deps:** `make deps`
- **Build (Cython):** `make build`
- **Test:** `make test` (requires running MySQL; `MYSQL_PASS` env var)
- **Lint + format (fix):** `make style`
- **Lint + format + types (check only):** `make check`
- **CI bundle:** `make ci`
- **Benchmark / examples:** `make benchmark` / `make example`

## Project Structure

- `asyncmy/` — driver source (Python + Cython `.pyx`)
- `tests/` — pytest suite (`test_*.py`)
- `examples/` — runnable usage samples
- `benchmark/` — performance scripts
- `build.py` — PDM custom build hook (Cython compilation)
- `conftest.py` — pytest fixtures

## Conventions

- **Commits:** Conventional Commits (`@commitlint/config-conventional`)
- **Lint targets:** `asyncmy/ tests/ examples/ conftest.py build.py`
- **Ruff:** line length 100; `FA`, `UP`, `RUF100` rules enabled

## Testing

- Tests live in `tests/` and are named `test_*.py`
- Async mode: `auto` (asyncio), session-scoped event loop
- Run a single test: `uv run pytest tests/test_connection.py::test_name`
- Requires a reachable MySQL instance; password via `MYSQL_PASS`

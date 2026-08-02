# Release Procedure

How to cut a release of `asyncmy2`. Publishing to PyPI is fully automated; the only
manual work is the version bump, the changelog entry, and creating the GitHub release.

> **Publishing is irreversible.** Creating the GitHub release uploads to PyPI, and PyPI
> never allows a version number to be reused. Confirm with the maintainer before running
> step 5 unless they explicitly asked for the release to be published.

## Where the version lives

`asyncmy/version.py` is the single source of truth. `pyproject.toml` reads it via
`[tool.pdm.version] source = "file"`, so nothing else needs editing:

- `uv.lock` records the project as `source = { editable = "." }` with no version field.
- `pyproject.toml` has no hardcoded version.

Versioning is `0.2.x`; bug fixes and dependency bumps get a patch bump.

## Steps

Run from a clean tree on `main`, with `main` up to date and CI green.

1. **Bump the version** in `asyncmy/version.py`:

   ```python
   __version__ = "0.2.21"
   ```

2. **Add a changelog section** at the top of `CHANGELOG.md`, directly under `# ChangeLog`.
   Newest version first, one bullet per user-facing change, most significant first, with
   issue/PR links. Internal churn (agent docs, gitignore, CI SHA pinning) is collapsed into
   a single "Bumped dependency and GitHub Actions versions." bullet — do not enumerate it.

   ```markdown
   ## 0.2.21

   - Fixed ... ([#24](https://github.com/vpmedia/asyncmy2/issues/24))
   - Bumped dependency and GitHub Actions versions.
   ```

   To see what actually changed since the last release:

   ```sh
   git log --oneline v0.2.20..HEAD
   ```

3. **Verify, then commit.** Run the suite first (needs a reachable MySQL, see below):

   ```sh
   make test
   git add asyncmy/version.py CHANGELOG.md
   git commit -m "chore(release): bump project version to v0.2.21"
   ```

4. **Push to `main`.** The repo commits releases directly to `main`; it is unprotected and
   the maintainer's own commits land there.

   ```sh
   git push origin main
   ```

5. **Create the GitHub release.** This is what triggers publishing. The tag is lightweight
   and created by GitHub here — do not push a tag by hand. Title and body follow the
   existing releases exactly; the anchor is the version with dots stripped (`0.2.21` →
   `#0221`):

   ```sh
   gh release create v0.2.21 --repo vpmedia/asyncmy2 --target main \
     --title "Release v0.2.21" \
     --notes "[Changelog](https://github.com/vpmedia/asyncmy2/blob/main/CHANGELOG.md#0221)"
   ```

## What the automation does

`.github/workflows/publish.yml` triggers on `release: created`:

- `build_wheels` — cibuildwheel across `macos-15-intel`, `macos-latest`, `ubuntu-latest`,
  `ubuntu-24.04-arm`, `windows-latest`, `windows-11-arm`
- `build_sdist` — `uv build` on `ubuntu-24.04`
- `upload` — needs both; publishes to PyPI via Trusted Publisher (`id-token: write`)

All jobs run in the `release` GitHub environment, which has no approval gate. The full
matrix takes about 20 minutes. A healthy release publishes 55 files: one sdist plus 54
wheels — cp310 through cp314 (including free-threaded `cp314t`) across the six OS targets.

## Verifying the release

```sh
gh run list --repo vpmedia/asyncmy2 --workflow publish.yml --limit 1
gh run view <run-id> --repo vpmedia/asyncmy2 --json status,conclusion,jobs \
  --jq '"\(.status) \(.conclusion)", (.jobs[] | "  \(.name): \(.conclusion)")'
```

Then confirm the artifacts landed and smoke-test the published wheel:

```sh
curl -sS https://pypi.org/pypi/asyncmy2/json | python -c "
import json, sys, collections
d = json.load(sys.stdin)
print('latest:', d['info']['version'])
print(collections.Counter(f['packagetype'] for f in d['releases']['0.2.21']))
"
uv venv /tmp/verify && VIRTUAL_ENV=/tmp/verify uv pip install --no-cache "asyncmy2==0.2.21"
```

PyPI's JSON API updates several minutes ahead of the CDN-cached simple index, so a fresh
install right after publishing can fail with "no version of asyncmy2==<version>" or report
a truncated set of ABI tags. That is propagation lag, not a broken release — confirm
against `https://pypi.org/simple/asyncmy2/` and retry.

If `upload` fails after wheels built successfully, re-running the job is safe **only if
nothing reached PyPI**. Once any artifact uploads, that version is burned and the fix is a
new patch version, not a retry.

## Other workflows

- `ci.yml` — runs on every push, Python 3.10–3.14 against a MySQL service container
- `check.yml` — same matrix, runs on pull requests

Neither gates the release; check `ci.yml` on `main` is green before step 5.

## Running tests locally

`make test` needs a reachable MySQL on `127.0.0.1:3306` as `root`. The password comes from
`MYSQL_PASS`, which `make` picks up from a local `.env` file if present, otherwise defaults
to `123456`:

```sh
MYSQL_PASS=<password> uv run pytest -q
```

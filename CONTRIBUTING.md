# Contributing to chiban-extract

Thanks for taking the time to contribute. Bug reports, regex edge cases, and
PDFs that break the extractor are especially welcome — this library is only
useful to the extent it covers real-world Japanese property documents.

## Reporting issues

When opening an issue, please include:

- A minimal text snippet (or a redacted PDF excerpt) that reproduces the
  problem. Real-world phrasing matters — synthetic test strings often do
  not reproduce PDF-extraction quirks.
- The expected vs. actual extraction output.
- The package version (`python -c "import chiban_extract; print(chiban_extract.__version__)"`).

If the input is sensitive, redact identifying numbers / names but keep the
surrounding Japanese phrasing intact — that's usually where the regex
mismatch lives.

## Development setup

```bash
git clone https://github.com/91st1213-blip/chiban-extract
cd chiban-extract
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check src tests
```

Python 3.10 or newer is required.

## Adding a regex pattern or fixing a quirk

Patterns in `src/chiban_extract/patterns.py` were tuned against hundreds of
real documents. If you change one:

1. Add a unit test that captures the new input shape in
   `tests/test_patterns.py` or `tests/test_extract.py`.
2. Run the full suite to confirm no regression
   (`pytest` should report all tests green).
3. In the PR description, describe the source of the input (press release,
   registry paper, brochure, etc.) — this helps reviewers reason about
   whether the new pattern generalizes.

NFKC normalization happens upstream of every regex, so patterns should be
written against normalized text (half-width digits, single-width kanji).

## Pull request checklist

- [ ] Tests added or updated for the behavior changed.
- [ ] `pytest` and `ruff check` pass locally.
- [ ] CHANGELOG.md updated under `[Unreleased]`.
- [ ] No new runtime dependencies without a brief justification in the PR
      description. (PyMuPDF is the only one; we'd like to keep it that
      way.)

## Code style

Ruff is the source of truth (`ruff check src tests`). Line length 120.
Public functions get type hints and a one-paragraph docstring describing
what they do, what inputs they accept, and what they return; no
multi-paragraph block comments.

## Releasing (maintainers)

1. Bump `version` in `pyproject.toml` and move the `[Unreleased]` notes in
   `CHANGELOG.md` under a new dated heading.
2. Tag `vX.Y.Z` and push.
3. `python -m build` then `twine upload dist/*`.
4. `gh release create vX.Y.Z dist/* --notes-file ...`.

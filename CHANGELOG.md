# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-06-12

Initial public release.

### Added
- `extract_from_text(text, ...)` — keyword-driven + pattern-driven address
  extraction over raw text, returning a ranked candidate list and a
  best-effort `best` match.
- `extract_from_pdf(source, ...)` — same pipeline over a PDF, accepting a
  filesystem path, an HTTP(S) URL, or raw bytes (PyMuPDF backend).
- Address kinds: residential indication (住居表示, ends with 号) and
  registered lot number (地番, 番地 / 番).
- Multi-property document support: `property_name` scopes extraction to a
  window after each occurrence of the name; `other_property_names` adds
  confusion warnings when similarly-named properties appear nearby.
- `known_address` validation: prefecture / city / ward / town tokens parsed
  from a known address are required to appear in the candidate.
- CLI `chiban-extract extract <path-or-url>` with `--json`,
  `--property-name`, `--known-address`, `--other-property-name`.
- NFKC normalization, canonicalization of full-width / half-width digits,
  kanji-numeral tolerance, and absorption of whitespace and line breaks
  injected by PDF text layers.
- MIT license, Python 3.10 / 3.11 / 3.12 / 3.13 support, CI on GitHub
  Actions, 56 unit tests.

[Unreleased]: https://github.com/91st1213-blip/chiban-extract/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/91st1213-blip/chiban-extract/releases/tag/v0.1.0

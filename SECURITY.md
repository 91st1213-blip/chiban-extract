# Security Policy

## Supported Versions

`chiban-extract` is pre-1.0 and tracks a single moving line of development.
Security fixes are made against the latest release on
[PyPI](https://pypi.org/project/chiban-extract/); older versions are not
patched separately.

| Version | Supported |
| ------- | --------- |
| latest  | ✅        |
| < latest | ❌       |

## Reporting a Vulnerability

Please **do not** open a public issue for security vulnerabilities.

Instead, use GitHub's private vulnerability reporting for this repository:
[Security → Report a vulnerability](https://github.com/91st1213-blip/chiban-extract/security/advisories/new).

Include:

- A description of the vulnerability and its potential impact
- Steps to reproduce (a minimal text/PDF sample if relevant)
- Any known mitigation

We aim to acknowledge reports within a few days and will credit reporters
in the release notes unless anonymity is requested.

## Scope Notes

`chiban-extract` parses untrusted PDF/text input with
[PyMuPDF](https://pypi.org/project/PyMuPDF/) and regular expressions. Reports
about denial-of-service via malicious PDFs (e.g. decompression bombs,
pathological regex backtracking) are welcome and in scope.

"""Text normalization helpers.

All extraction regexes in this package assume NFKC-normalized text
(full-width digits/letters folded to half-width).
"""

from __future__ import annotations

import re
import unicodedata


def normalize_text(text: str) -> str:
    """Return *text* normalized with Unicode NFKC."""
    return unicodedata.normalize("NFKC", text or "")


def canonicalize_address(s: str) -> str:
    """Remove all whitespace from an extracted address string.

    PDF text extraction frequently injects spaces and line breaks between
    digits and counters such as 番 / 号 / 丁目; canonicalizing makes
    candidates comparable.
    """
    return re.sub(r"\s+", "", s)

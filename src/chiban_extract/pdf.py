"""PDF reading: local path, URL, or raw bytes → normalized text + page count.

PyMuPDF is imported lazily so that users who only call the text-based APIs
(:func:`chiban_extract.extract_from_text` etc.) never pay the import cost.
"""

from __future__ import annotations

import urllib.request
from pathlib import Path

from .models import PdfDocument
from .normalize import normalize_text

_USER_AGENT = "Mozilla/5.0 (compatible; chiban-extract)"
_TIMEOUT = 30


def _fetch_url(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
    with urllib.request.urlopen(req, timeout=_TIMEOUT) as resp:  # noqa: S310
        return resp.read()


def read_pdf(source: str | Path | bytes) -> PdfDocument:
    """Read a PDF from a file path, an http(s) URL, or raw bytes.

    Returns the NFKC-normalized full text and the page count.
    """
    if isinstance(source, bytes):
        data = source
    elif isinstance(source, (str, Path)) and str(source).startswith(("http://", "https://")):
        data = _fetch_url(str(source))
    else:
        data = Path(source).read_bytes()

    import fitz  # PyMuPDF

    doc = fitz.open(stream=data, filetype="pdf")
    try:
        text = "\n".join(page.get_text() for page in doc)
        page_count = len(doc)
    finally:
        doc.close()
    return PdfDocument(text=normalize_text(text), page_count=page_count)

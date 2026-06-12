"""chiban-extract: Japanese street addresses & land lot numbers out of text and PDFs.

Quick start::

    from chiban_extract import extract_from_pdf

    result = extract_from_pdf("document.pdf", known_address="東京都港区")
    print(result.best.address if result.best else "not found")
"""

from .extract import (
    extract_address_for_property,
    extract_preferred_address,
    find_address_candidates,
)
from .models import (
    AddressCandidate,
    AddressKind,
    AddressMatch,
    AddressTokens,
    ExtractionResult,
    PdfDocument,
)
from .normalize import canonicalize_address, normalize_text
from .pdf import read_pdf
from .pipeline import extract_from_pdf, extract_from_text
from .tokens import has_block_number, parse_address_tokens

__version__ = "0.1.0"

__all__ = [
    "AddressCandidate",
    "AddressKind",
    "AddressMatch",
    "AddressTokens",
    "ExtractionResult",
    "PdfDocument",
    "canonicalize_address",
    "extract_address_for_property",
    "extract_from_pdf",
    "extract_from_text",
    "extract_preferred_address",
    "find_address_candidates",
    "has_block_number",
    "normalize_text",
    "parse_address_tokens",
    "read_pdf",
    "__version__",
]

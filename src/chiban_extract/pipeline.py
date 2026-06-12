"""High-level pipeline: text or PDF → best address + ranked candidates."""

from __future__ import annotations

from pathlib import Path

from .extract import (
    _address_kind,
    extract_address_for_property,
    extract_preferred_address,
    find_address_candidates,
)
from .models import AddressCandidate, ExtractionResult
from .normalize import canonicalize_address, normalize_text
from .pdf import read_pdf
from .tokens import parse_address_tokens


def extract_from_text(
    text: str,
    *,
    page_count: int | None = None,
    property_name: str | None = None,
    known_address: str | None = None,
    other_property_names: list[str] | None = None,
) -> ExtractionResult:
    """Run address extraction over raw text.

    Strategy: keyword-driven extraction (住居表示 preferred, 地番 fallback)
    wins when it finds something; otherwise the top pattern-driven candidate
    is used. All candidates are returned for inspection either way.
    """
    text_n = normalize_text(text)
    warnings: list[str] = []

    expected = parse_address_tokens(known_address) if known_address else None
    candidates = find_address_candidates(text_n, expected)

    preferred: str | None = None
    if property_name:
        match = extract_address_for_property(
            text_n,
            property_name,
            known_address=known_address,
            other_property_names=other_property_names,
        )
        if match:
            preferred = match.address
            warnings.extend(match.warnings)
    else:
        preferred = extract_preferred_address(text_n, known_address=known_address)

    best: AddressCandidate | None = None
    if preferred:
        canon = canonicalize_address(preferred)
        best = next(
            (c for c in candidates if c.address == canon),
            AddressCandidate(
                address=canon, kind=_address_kind(canon), position=-1, near_keyword=True
            ),
        )
    elif candidates:
        best = candidates[0]

    return ExtractionResult(
        candidates=candidates,
        best=best,
        page_count=page_count,
        warnings=warnings,
    )


def extract_from_pdf(
    source: str | Path | bytes,
    *,
    property_name: str | None = None,
    known_address: str | None = None,
    other_property_names: list[str] | None = None,
) -> ExtractionResult:
    """Read a PDF (path / URL / bytes) and extract addresses from it."""
    doc = read_pdf(source)
    return extract_from_text(
        doc.text,
        page_count=doc.page_count,
        property_name=property_name,
        known_address=known_address,
        other_property_names=other_property_names,
    )

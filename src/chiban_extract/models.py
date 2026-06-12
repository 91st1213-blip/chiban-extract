"""Dataclasses and enums shared across the package."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class AddressKind(str, Enum):
    """Whether an extracted address is a residential indication or a lot number.

    - JUKYO (住居表示): "...N番M号" — the official street address of a building.
    - CHIBAN (地番): "...N番地M" / "...N番" — the registered land lot number.
    """

    JUKYO = "jukyo"
    CHIBAN = "chiban"


@dataclass(frozen=True)
class AddressTokens:
    """Coarse components of a Japanese address used for cross-validation.

    All fields may be empty strings when the component is absent or unknown.
    """

    pref: str = ""  # 都道府県
    city: str = ""  # 市/郡 (empty for Tokyo 23 wards)
    ward: str = ""  # 区
    town: str = ""  # 町名 (up to the first block digit)

    def to_dict(self) -> dict:
        return {"pref": self.pref, "city": self.city, "ward": self.ward, "town": self.town}


@dataclass(frozen=True)
class AddressCandidate:
    """A single address string found in the text."""

    address: str
    kind: AddressKind
    position: int  # character offset in the normalized text (-1 if synthesized)
    near_keyword: bool  # found within 200 chars after an address keyword

    def to_dict(self) -> dict:
        return {
            "address": self.address,
            "kind": self.kind.value,
            "position": self.position,
            "near_keyword": self.near_keyword,
        }


@dataclass(frozen=True)
class AddressMatch:
    """Result of name-scoped extraction (:func:`extract_address_for_property`)."""

    address: str
    kind: AddressKind
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {"address": self.address, "kind": self.kind.value, "warnings": list(self.warnings)}


@dataclass(frozen=True)
class ExtractionResult:
    """High-level result returned by :func:`extract_from_pdf` / :func:`extract_from_text`."""

    candidates: list[AddressCandidate]
    best: AddressCandidate | None
    page_count: int | None
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "candidates": [c.to_dict() for c in self.candidates],
            "best": self.best.to_dict() if self.best else None,
            "page_count": self.page_count,
            "warnings": list(self.warnings),
        }


@dataclass(frozen=True)
class PdfDocument:
    """NFKC-normalized text content of a PDF plus its page count."""

    text: str
    page_count: int

"""Address extraction from Japanese text.

Two complementary strategies:

1. :func:`extract_preferred_address` — keyword-driven. Looks for an address
   right after 「住居表示」 (residential indication, preferred) or
   「所在地」/「地番」 (lot number, fallback), optionally scoped to the
   vicinity of a property name for multi-property documents.
2. :func:`find_address_candidates` — pattern-driven. Scans the whole text
   with a generic address regex and ranks candidates that appear near
   address keywords first.

Both validate candidates against an optionally provided known address
(prefecture / city / ward / town containment) to reject addresses that
belong to other properties or other parties mentioned in the document.
"""

from __future__ import annotations

import re

from .models import AddressCandidate, AddressKind, AddressMatch, AddressTokens
from .normalize import canonicalize_address, normalize_text
from .patterns import ADDR_RE, ADDRESS_KEYWORDS, CHIBAN_RE, JUKYO_RE
from .tokens import parse_address_tokens

# How far after a keyword a candidate may start and still count as "near".
_KEYWORD_WINDOW = 200
# How much context is scanned after a property-name occurrence.
_PROPERTY_WINDOW = 2500

WARN_OTHER_PROPERTY_NEARBY = "another property with a similar name appears nearby: {name}"


def _address_kind(address: str) -> AddressKind:
    return AddressKind.JUKYO if "号" in address else AddressKind.CHIBAN


def _clean_name(name: str) -> str:
    """Strip parenthesized suffixes and whitespace from a property name."""
    cleaned = re.sub(r"[（(].*?[)）]", "", name)
    return re.sub(r"\s", "", cleaned)


def find_address_candidates(
    text: str,
    expected: AddressTokens | None = None,
) -> list[AddressCandidate]:
    """Scan *text* for address-like strings and rank them.

    Candidates appearing within 200 chars after an address keyword
    (地番/住居表示/所在地/住所) are ranked first. When *expected* tokens are
    given, candidates whose prefecture/city/ward/town do not contain the
    expected tokens are dropped.
    """
    text_n = normalize_text(text)
    raw: list[tuple[int, str]] = []
    seen: set[str] = set()
    for m in ADDR_RE.finditer(text_n):
        s = canonicalize_address(m.group(0))
        if s in seen:
            continue
        seen.add(s)
        if expected:
            # Every token present in the known address must reappear.
            if expected.pref and not s.startswith(expected.pref):
                continue
            if expected.city and expected.city not in s:
                continue
            if expected.ward and expected.ward not in s:
                continue
            if expected.town and expected.town not in s:
                continue
        raw.append((m.start(), s))

    keyword_positions = sorted(
        m.start() for kw in ADDRESS_KEYWORDS for m in re.finditer(kw, text_n)
    )

    def near_keyword(pos: int) -> bool:
        return any(0 <= pos - kp <= _KEYWORD_WINDOW for kp in keyword_positions)

    candidates = [
        AddressCandidate(
            address=s, kind=_address_kind(s), position=pos, near_keyword=near_keyword(pos)
        )
        for pos, s in raw
    ]
    near = [c for c in candidates if c.near_keyword]
    far = [c for c in candidates if not c.near_keyword]
    return near + far


def extract_preferred_address(
    text: str,
    property_name: str | None = None,
    known_address: str | None = None,
) -> str | None:
    """Extract the best address near explicit keywords.

    Searches for a residential indication (住居表示, ends with 号) first and
    falls back to a lot number (地番). When *property_name* is given, only
    text within 2,500 chars after each occurrence of the name is searched —
    essential for multi-property documents. When *known_address* is given,
    the prefecture and city/ward of the candidate must match it.
    """
    text_clean = re.sub(r"[\s\n]", "", normalize_text(text))

    expected = parse_address_tokens(known_address) if known_address else AddressTokens()

    def token_ok(cand: str) -> bool:
        if expected.pref and not cand.startswith(expected.pref):
            return False
        if expected.city and expected.city not in cand:
            return False
        if expected.ward and expected.ward not in cand:
            return False
        return True

    if property_name:
        name_clean = _clean_name(property_name)
        windows = [
            text_clean[m.start():m.start() + _PROPERTY_WINDOW]
            for m in re.finditer(re.escape(name_clean[:18]), text_clean)
        ]
    else:
        windows = [text_clean]

    for sub in windows:
        # 1. Address right after 「住居表示」 (number ends with 号).
        for sm in re.finditer(r"住居表示", sub):
            ctx = sub[sm.end():sm.end() + 250]
            jm = JUKYO_RE.search(ctx[:200])
            if jm and token_ok(jm.group(1)):
                return jm.group(1)
        # 2. Fallback: lot number right after 「土地所在地」/「地番」.
        for sm in re.finditer(r"土地?所在地|土地?地番|^所在地$", sub):
            ctx = sub[sm.end():sm.end() + 250]
            cm = CHIBAN_RE.search(ctx[:200])
            if cm and token_ok(cm.group(1)):
                return cm.group(1).strip()
    return None


def extract_address_for_property(
    text: str,
    property_name: str,
    known_address: str | None = None,
    other_property_names: list[str] | None = None,
) -> AddressMatch | None:
    """Name-scoped extraction with confusion checks for multi-property documents.

    When a document covers several properties whose names share a prefix
    (e.g. 「サンプル戸越公園」 vs 「サンプル東大井」), pass the other names
    via *other_property_names*; a warning is added when one of them appears
    near the target property's occurrences.
    """
    addr = extract_preferred_address(text, property_name=property_name, known_address=known_address)
    if not addr:
        return None

    warnings: list[str] = []
    text_clean = re.sub(r"[\s\n]", "", normalize_text(text))
    name_clean = _clean_name(property_name)

    for other in other_property_names or []:
        other_clean = _clean_name(other)
        if other_clean == name_clean:
            continue
        for m in re.finditer(re.escape(name_clean[:6]), text_clean):
            sub = text_clean[m.start():m.start() + 1500]
            if other_clean[:10] in sub:
                warnings.append(WARN_OTHER_PROPERTY_NEARBY.format(name=other))
                break

    return AddressMatch(address=addr, kind=_address_kind(addr), warnings=warnings)

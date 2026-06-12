"""Coarse tokenization of Japanese address strings.

These helpers split an address into prefecture / city / ward / town tokens so
that an address extracted from a PDF can be cross-checked against an address
that is already known (e.g. from a property database). Tokenization is
heuristic — it does not depend on a full address dictionary — which is
sufficient for containment checks.
"""

from __future__ import annotations

import re

from .models import AddressTokens
from .normalize import normalize_text

PREF_RE = re.compile(r"(東京都|北海道|(?:京都|大阪)府|.{2,3}県)")

_CITY_RE = re.compile(r"([^\s。、，,]{1,15}?(?:市|郡))")
_WARD_RE = re.compile(r"([^\s。、，,]{1,10}?区)")
# Town: everything up to a block/chome numeral. Kanji numerals may legitimately
# appear inside town names (北一条西, 六本木, 三芳町...), so we only stop at a
# numeral run that is followed by 丁目/番, or at an ASCII digit.
_TOWN_RE = re.compile(
    r"([^0-9].*?)(?=\s*[0-9一二三四五六七八九十百千]+\s*(?:丁目|番)|[0-9]|$)"
)

# Block-number detection: 「1番9」「788番地」「5番5号」「1-2-3」(after NFKC).
_BLOCK_NUMBER_RE = re.compile(
    r"[0-9]+\s*番(?:地)?(?:\s*[0-9]+)?(?:\s*号)?"
    r"|[0-9]+\s*[-‐−―ー]\s*[0-9]+"
)


def parse_address_tokens(addr: str) -> AddressTokens:
    """Split *addr* into prefecture / city / ward / town tokens.

    Any component that cannot be identified is returned as an empty string,
    so the result is always safe to use for containment checks.

    >>> parse_address_tokens("熊本県熊本市中央区下通二丁目1番9")
    AddressTokens(pref='熊本県', city='熊本市', ward='中央区', town='下通')
    """
    a = normalize_text(addr).strip()
    m = PREF_RE.match(a)
    pref = m.group(1) if m else ""
    rest = a[len(pref):]

    city = ""
    m = _CITY_RE.match(rest)
    if m:
        city = m.group(1)
        rest = rest[len(city):]

    ward = ""
    m = _WARD_RE.match(rest)
    if m:
        ward = m.group(1)
        rest = rest[len(ward):]

    town = ""
    m = _TOWN_RE.match(rest)
    if m:
        town = m.group(1)

    return AddressTokens(pref=pref, city=city, ward=ward, town=town)


def has_block_number(addr: str) -> bool:
    """Return True if *addr* contains a block/lot number.

    Used to decide whether an address is precise enough (e.g. 「1番9」,
    「788番地」, 「5番5号」, 「1-2-3」) or stops at the town / 丁目 level.

    >>> has_block_number("東京都港区南青山1丁目1番1号")
    True
    >>> has_block_number("東京都港区南青山一丁目")
    False
    """
    return bool(_BLOCK_NUMBER_RE.search(normalize_text(addr)))

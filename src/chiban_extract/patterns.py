"""Regex patterns for Japanese addresses.

These patterns were battle-tested against hundreds of real-world Japanese
property documents (PDF press releases, contracts, registry papers). Do not
"simplify" character classes without running the full test suite — every
quirk (whitespace absorption, kanji numerals, optional city/ward) exists
because real documents require it.

All patterns assume NFKC-normalized input (see :mod:`chiban_extract.normalize`).
"""

from __future__ import annotations

import re

# Generic address pattern (lot number or street address).
# Examples it must match:
#   熊本県熊本市中央区下通二丁目1番9
#   東京都港区南青山1丁目1番1号
#   東京都千代田区内神田二丁目5番5号
# PDF text extraction often injects spaces/newlines between digits and
# 番/号/丁目, so the pattern absorbs interior whitespace.
# Both city and ward are optional (Tokyo 23 wards have no city; designated
# cities have a ward). The tail accepts a block number, a 丁目-only address,
# or an aza (字) name.
ADDR_RE = re.compile(
    r"(?P<pref>東京都|北海道|(?:京都|大阪)府|.{2,3}県)"
    r"\s*(?P<city>[^\s。、，,]{1,15}?(?:市|郡))?"
    r"\s*(?P<ward>[^\s。、，,]{1,10}?区)?"
    r"\s*(?P<rest>[^\s。、，,（）()「」『』【】〔〕\d]{1,25}?"
    r"(?:\s*[0-9一二三四五六七八九十百千]+\s*丁目)?"
    r"(?:"
    r"\s*[0-9一二三四五六七八九十百千]+\s*(?:番(?:地)?\s*[0-9一二三四五六七八九十]*\s*(?:号)?|[\-－―ー]\s*[0-9一二三四五六七八九十]+(?:\s*[\-－―ー]\s*[0-9一二三四五六七八九十]+)?)"
    r"|\s*[0-9一二三四五六七八九十百千]+\s*丁目"
    r"))"
)

# Residential indication (住居表示): prefecture + ... + 「番N号」 (ends with 号).
JUKYO_RE = re.compile(
    r"((?:東京都|北海道|(?:京都|大阪)府|.{2,3}県)"
    r"[^\s。、，,（）()「」『』【】〔〕]{2,50}?"
    r"(?:[0-9一二三四五六七八九十百千]+\s*丁目)?"
    r"\s*[0-9一二三四五六七八九十百千]+\s*番\s*[0-9一二三四五六七八九十]*\s*号)"
)

# Lot number (地番): 「番地N」「番N」 without 号; tolerates suffixes like 「他N筆」.
CHIBAN_RE = re.compile(
    r"((?:東京都|北海道|(?:京都|大阪)府|.{2,3}県)"
    r"[^\s。、，,（）()「」『』【】〔〕]{2,50}?"
    r"(?:[0-9一二三四五六七八九十百千]+\s*丁目)?"
    r"\s*[0-9一二三四五六七八九十百千]+\s*(?:番地?|番)[\s0-9一二三四五六七八九十他筆]*)"
)

# Keywords whose vicinity is preferred when ranking address candidates.
ADDRESS_KEYWORDS = ["地番", "住居表示", "所在地", "住所"]

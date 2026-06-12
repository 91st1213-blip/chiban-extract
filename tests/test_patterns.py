"""Table-driven tests for the address regexes."""

import pytest

from chiban_extract.normalize import canonicalize_address, normalize_text
from chiban_extract.patterns import ADDR_RE, CHIBAN_RE, JUKYO_RE


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("熊本県熊本市中央区下通二丁目1番9", "熊本県熊本市中央区下通二丁目1番9"),
        ("東京都港区南青山1丁目1番1号", "東京都港区南青山1丁目1番1号"),
        ("東京都千代田区内神田二丁目5番5号", "東京都千代田区内神田二丁目5番5号"),
        # Tokyo 23 wards: no city component.
        ("東京都品川区東大井2丁目22番15号", "東京都品川区東大井2丁目22番15号"),
        # designated city: city + ward.
        ("大阪府大阪市北区梅田三丁目3番3号", "大阪府大阪市北区梅田三丁目3番3号"),
        # whitespace injected between digits and counters.
        ("東京都千代田区内神田二丁目 5 番 5 号", "東京都千代田区内神田二丁目5番5号"),
        # 丁目-only address.
        ("東京都港区南青山一丁目", "東京都港区南青山一丁目"),
        # hyphen style.
        ("東京都新宿区西新宿2-8-1", "東京都新宿区西新宿2-8-1"),
    ],
)
def test_addr_re_matches(text: str, expected: str):
    m = ADDR_RE.search(normalize_text(text))
    assert m, f"no match in {text!r}"
    assert canonicalize_address(m.group(0)) == expected


@pytest.mark.parametrize(
    "text",
    [
        "電話番号 03-1234-5678",
        "販売価格 5,000百万円",
        "2026年6月1日",
    ],
)
def test_addr_re_rejects_non_addresses(text: str):
    m = ADDR_RE.search(normalize_text(text))
    assert m is None, f"unexpected match {m.group(0) if m else ''!r} in {text!r}"


def test_jukyo_vs_chiban_boundary():
    # 「番N号」 → residential indication.
    assert JUKYO_RE.search("東京都港区南青山1丁目1番1号")
    # 「番地N」 without 号 → lot number, not jukyo.
    assert not JUKYO_RE.search("埼玉県入間郡三芳町大字上鹿山788番地")
    assert CHIBAN_RE.search("埼玉県入間郡三芳町大字上鹿山788番地")


def test_chiban_re_accepts_extra_lots():
    m = CHIBAN_RE.search("埼玉県入間郡三芳町大字上鹿山788番地 他3筆")
    assert m
    assert "788番地" in m.group(1)

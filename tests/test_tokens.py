import pytest

from chiban_extract.tokens import has_block_number, parse_address_tokens


@pytest.mark.parametrize(
    ("addr", "pref", "city", "ward", "town"),
    [
        ("熊本県熊本市中央区下通二丁目1番9", "熊本県", "熊本市", "中央区", "下通"),
        ("東京都千代田区内神田二丁目5番5号", "東京都", "", "千代田区", "内神田"),
        ("東京都港区南青山1丁目1番1号", "東京都", "", "港区", "南青山"),
        ("大阪府大阪市北区梅田三丁目3番3号", "大阪府", "大阪市", "北区", "梅田"),
        ("埼玉県入間郡三芳町大字上鹿山788番地", "埼玉県", "入間郡", "", "三芳町大字上鹿山"),
        ("北海道札幌市中央区北一条西3丁目", "北海道", "札幌市", "中央区", "北一条西"),
        ("", "", "", "", ""),
    ],
)
def test_parse_address_tokens(addr, pref, city, ward, town):
    t = parse_address_tokens(addr)
    assert (t.pref, t.city, t.ward, t.town) == (pref, city, ward, town)


def test_parse_address_tokens_fullwidth_input():
    # full-width digits are NFKC-folded before tokenizing
    t = parse_address_tokens("東京都港区南青山１丁目")
    assert t.ward == "港区"
    assert t.town == "南青山"


@pytest.mark.parametrize(
    ("addr", "expected"),
    [
        ("東京都港区南青山1丁目1番1号", True),
        ("埼玉県入間郡三芳町大字上鹿山788番地", True),
        ("熊本県熊本市中央区下通二丁目1番9", True),
        ("東京都新宿区西新宿2-8-1", True),
        ("東京都新宿区西新宿２－８－１", True),  # full-width
        ("東京都港区南青山一丁目", False),
        ("東京都港区南青山", False),
        ("", False),
    ],
)
def test_has_block_number(addr, expected):
    assert has_block_number(addr) is expected

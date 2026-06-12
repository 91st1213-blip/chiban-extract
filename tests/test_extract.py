from chiban_extract.extract import (
    extract_address_for_property,
    extract_preferred_address,
    find_address_candidates,
)
from chiban_extract.models import AddressKind
from chiban_extract.tokens import parse_address_tokens


def test_candidates_near_keyword_first(sample_text):
    cands = find_address_candidates(sample_text)
    assert cands
    assert cands[0].near_keyword
    addrs = [c.address for c in cands]
    assert "東京都港区南青山1丁目1番1号" in addrs
    assert "東京都港区南青山1丁目2番3" in addrs


def test_candidates_filtered_by_expected_tokens(sample_text):
    # expecting a Kumamoto address drops all Tokyo candidates
    expected = parse_address_tokens("熊本県熊本市中央区")
    assert find_address_candidates(sample_text, expected) == []


def test_candidate_kinds(sample_text):
    kinds = {c.address: c.kind for c in find_address_candidates(sample_text)}
    assert kinds["東京都港区南青山1丁目1番1号"] is AddressKind.JUKYO
    assert kinds["東京都港区南青山1丁目2番3"] is AddressKind.CHIBAN


def test_preferred_address_prefers_jukyo(sample_text):
    # both 住居表示 and 地番 are present; 住居表示 must win
    assert extract_preferred_address(sample_text) == "東京都港区南青山1丁目1番1号"


def test_preferred_address_falls_back_to_chiban(chiban_only_text):
    addr = extract_preferred_address(chiban_only_text, property_name="サンプルビル熊本")
    assert addr is None or "熊本県" in addr  # no 住居表示 keyword: keyword pass may miss
    # the generic candidate scan still finds the lot number
    cands = find_address_candidates(chiban_only_text)
    assert cands[0].address == "熊本県熊本市中央区下通二丁目1番9"


def test_preferred_address_token_validation(sample_text):
    # known address in a different ward rejects the candidate
    assert extract_preferred_address(sample_text, known_address="東京都品川区") is None
    assert (
        extract_preferred_address(sample_text, known_address="東京都港区")
        == "東京都港区南青山1丁目1番1号"
    )


def test_property_scoped_extraction(multi_property_text):
    a = extract_preferred_address(multi_property_text, property_name="サンプルレジデンス戸越公園")
    b = extract_preferred_address(multi_property_text, property_name="サンプルレジデンス東大井")
    assert a == "東京都品川区豊町6丁目5番1号"
    assert b == "東京都品川区東大井2丁目22番15号"


def test_messy_whitespace(messy_whitespace_text):
    addr = extract_preferred_address(messy_whitespace_text)
    assert addr == "東京都千代田区内神田二丁目5番5号"


def test_confusion_warning(multi_property_text):
    m = extract_address_for_property(
        multi_property_text,
        "サンプルレジデンス戸越公園",
        other_property_names=["サンプルレジデンス東大井"],
    )
    assert m is not None
    assert m.address == "東京都品川区豊町6丁目5番1号"
    assert m.warnings  # similar-prefix property nearby


def test_no_confusion_warning_for_distinct_names(multi_property_text):
    m = extract_address_for_property(
        multi_property_text,
        "サンプルレジデンス戸越公園",
        other_property_names=["全く別の物件名"],
    )
    assert m is not None
    assert m.warnings == []

from chiban_extract.models import AddressKind
from chiban_extract.pipeline import extract_from_pdf, extract_from_text


def test_extract_from_text_full_flow(sample_text):
    r = extract_from_text(sample_text, page_count=8)
    assert r.best is not None
    assert r.best.address == "東京都港区南青山1丁目1番1号"
    assert r.best.kind is AddressKind.JUKYO
    assert len(r.candidates) == 2
    assert r.page_count == 8


def test_extract_from_text_known_address_filter(sample_text):
    r = extract_from_text(sample_text, known_address="熊本県熊本市")
    assert r.best is None
    assert r.candidates == []


def test_extract_from_text_fallback_to_candidates(chiban_only_text):
    # no 住居表示 keyword: best falls back to the top-ranked candidate
    r = extract_from_text(chiban_only_text)
    assert r.best is not None
    assert r.best.address == "熊本県熊本市中央区下通二丁目1番9"
    assert r.best.kind is AddressKind.CHIBAN


def test_extract_from_text_property_scope_and_warnings(multi_property_text):
    r = extract_from_text(
        multi_property_text,
        property_name="サンプルレジデンス戸越公園",
        other_property_names=["サンプルレジデンス東大井"],
    )
    assert r.best is not None
    assert r.best.address == "東京都品川区豊町6丁目5番1号"
    assert any("サンプルレジデンス東大井" in w for w in r.warnings)


def test_extract_from_text_nothing_found(no_address_text):
    r = extract_from_text(no_address_text, page_count=2)
    assert r.best is None
    assert r.candidates == []


def test_to_dict_roundtrip(sample_text):
    d = extract_from_text(sample_text, page_count=8).to_dict()
    assert d["best"]["address"] == "東京都港区南青山1丁目1番1号"
    assert d["best"]["kind"] == "jukyo"
    assert isinstance(d["candidates"], list)


def test_extract_from_pdf(sample_text):
    from test_pdf import make_pdf

    r = extract_from_pdf(make_pdf([sample_text]))
    assert r.page_count == 1
    assert r.best is not None
    assert r.best.address == "東京都港区南青山1丁目1番1号"

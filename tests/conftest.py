"""Synthetic Japanese property-document texts.

No real PDFs are bundled; these fixtures reproduce the textual quirks
(whitespace injection, kanji numerals, table-ish layout) that the extraction
logic must survive.
"""

import pytest


@pytest.fixture
def sample_text() -> str:
    """A document with both a residential indication and a lot number."""
    return (
        "物件概要書\n"
        "物件名称 サンプルレジデンス南青山\n"
        "所在地 (住居表示) 東京都港区南青山1丁目1番1号\n"
        "地番 東京都港区南青山1丁目2番3\n"
        "延床面積 5,000平米\n"
    )


@pytest.fixture
def chiban_only_text() -> str:
    """A document that gives only a lot number, no 住居表示 keyword."""
    return (
        "物件概要書\n"
        "物件名称 サンプルビル熊本\n"
        "所在地 (地番) 熊本県熊本市中央区下通二丁目1番9\n"
        "敷地面積 1,200平米\n"
    )


@pytest.fixture
def no_address_text() -> str:
    """A document containing no address at all."""
    return (
        "改訂履歴のお知らせ\n"
        "本書は文書管理規程の改訂についてお知らせするものです。\n"
        "詳細は管理担当までお問い合わせください。\n"
    )


@pytest.fixture
def multi_property_text() -> str:
    """Two properties with a shared name prefix in one document."""
    return (
        "物件一覧\n"
        "1. サンプルレジデンス戸越公園\n"
        "所在地 (住居表示) 東京都品川区豊町6丁目5番1号\n"
        "2. サンプルレジデンス東大井\n"
        "所在地 (住居表示) 東京都品川区東大井2丁目22番15号\n"
    )


@pytest.fixture
def messy_whitespace_text() -> str:
    """Digits separated from counters by spaces/newlines, as PDF layers do."""
    return (
        "物件概要\n"
        "所在地 (住居表示)\n"
        "東京都千代田区内神田二丁目 5 番\n5 号\n"
    )

# chiban-extract

Extract Japanese street addresses (住居表示) and registered land lot numbers
(地番) from plain text and PDFs.

日本語のテキスト・PDFから住居表示と地番を抽出する Python ライブラリ & CLI です。

[English](#english) | [日本語](#日本語)

---

## English

### Why?

Japanese property documents — contracts, registry papers, brochures, press
releases — write a property's location in inconsistent formats: as a
residential indication (住居表示, `…1番1号`), as a registered lot number
(地番, `…788番地 他3筆`), with kanji numerals, or with whitespace and line
breaks injected by a PDF text layer. Generic address parsers choke on this;
`chiban-extract`'s regexes were battle-tested against hundreds of real
documents.

It also solves the problems *around* extraction:

- **Multi-property documents** — when one document covers several properties
  with similar names, extraction can be scoped to the vicinity of one
  property name, with confusion warnings.
- **Validation against known data** — candidates are cross-checked against a
  known prefecture / city / ward so you don't accidentally pick up another
  party's address mentioned in the same document.
- **Candidate ranking** — every address-like string is returned, with those
  near an address keyword (住居表示 / 所在地 / 地番 / 住所) ranked first.

### Install

```bash
pip install chiban-extract
```

Requires Python 3.10+. The only dependency is PyMuPDF (and only the
text-based APIs can be used without it ever being imported).

### Quick start

```python
from chiban_extract import extract_from_pdf, extract_from_text

result = extract_from_pdf("document.pdf")                  # path, URL, or bytes
print(result.best.address if result.best else None)        # 東京都港区南青山1丁目1番1号
print(result.best.kind if result.best else None)           # AddressKind.JUKYO / CHIBAN
for c in result.candidates:
    print(c.address, c.kind, c.near_keyword)
```

Scoped extraction for multi-property documents, validated against a known
address:

```python
result = extract_from_pdf(
    "multi_property.pdf",
    property_name="サンプルレジデンス戸越公園",
    known_address="東京都品川区",
    other_property_names=["サンプルレジデンス東大井"],
)
```

### CLI

```bash
chiban-extract extract document.pdf --json
chiban-extract extract https://example.com/document.pdf --known-address "東京都港区"
chiban-extract extract document.pdf --property-name "サンプルビル" --known-address "東京都港区"
```

Exit codes: `0` success, `1` nothing found, `2` input error.

### How it works

1. PDF text is extracted with PyMuPDF and NFKC-normalized.
2. A keyword-driven pass looks for an address right after 「住居表示」
   (preferred — it identifies the building) and falls back to lot numbers
   after 「所在地」/「地番」.
3. A pattern-driven pass collects all address-like strings, ranking those
   within 200 chars of an address keyword first.
4. Candidates that contradict the known prefecture / city / ward are dropped.

### License

MIT

---

## 日本語

### 概要

不動産関連文書(契約書・登記資料・パンフレット・プレスリリース等)に
記載される所在地は、住居表示(`…1番1号`)・地番(`…788番地 他3筆`)・
漢数字丁目・PDFテキスト層由来の空白/改行混入などフォーマットが安定しません。
本ライブラリの正規表現は数百件の実文書で鍛えたもので、抽出まわりの
周辺問題もまとめて解決します。

- **複数物件文書対応** — 物件名近傍にスコープした抽出と、類似名物件との
  混同警告。
- **既知住所との突合** — 都道府県/市/区トークンで候補を検証し、同一文書中の
  別当事者住所の誤抽出を防ぎます。
- **候補ランキング** — 住所らしき文字列を全件返し、キーワード
  (住居表示/所在地/地番/住所)近傍のものを優先します。

### インストール

```bash
pip install chiban-extract
```

Python 3.10 以上が必要です。依存は PyMuPDF のみです。

### 使い方

```python
from chiban_extract import extract_from_text, extract_from_pdf

result = extract_from_pdf("document.pdf", known_address="東京都港区")
if result.best:
    print(result.best.address, result.best.kind)  # jukyo (住居表示) / chiban (地番)
```

CLI:

```bash
chiban-extract extract document.pdf --json
chiban-extract extract document.pdf --known-address "東京都港区"
```

### 抽出ロジック

1. PyMuPDF で全文抽出 → NFKC 正規化
2. 「住居表示」直後の住所を優先抽出(建物を一意に示すため)、無ければ
   「所在地」「地番」直後の地番にフォールバック
3. 汎用住所パターンで全候補を収集し、キーワード近傍(200字以内)を優先
4. 既知住所の都道府県/市/区/町トークンと矛盾する候補を除外

### ライセンス

MIT

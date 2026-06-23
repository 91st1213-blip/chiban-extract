# project.md — chiban-extract

リポジトリの目的・スコープ・運営方針。

## 目的

J-REIT / 不動産 PDF から **住居表示と地番** を抽出するロジックを汎用化した個人 OSS。「○○ 5 丁目 12 番 3 号」「○○一丁目 1 番 1 号 (地番)」など、日本の不動産開示で出てくる多様な住所表記を正規化する。

## スコープ

- **入力**: テキスト、または PDF (PyMuPDF / `fitz` 経由)
- **出力**: 住居表示 / 地番 のリスト (信頼度付き)
- **対応形式**:
  - 住居表示 (例: 港区赤坂 1 丁目 12 番 32 号)
  - 地番 (例: 港区赤坂 1 丁目 12 番地 32)
  - 略式 / 全角 / 半角混在
  - 注書きパターン (「地番」「住居表示」明示)

## やらないこと

- **国際住所**: 日本国内の住所形式のみ
- **緯度経度変換 (geocoding)**: chiban-extract の責務は文字列抽出のみ。geocoding は呼び出し側で GSI / Google などを使う
- **PDF 以外の OCR**: 画像 PDF は呼び出し側で OCR してから渡す
- **手入力データの校正**: 「正しい住所」かの判定はせず、抽出のみ

## ステークホルダー

- **オーナー**: 個人 (Takumi Sugimoto / 91st1213@gmail.com)
- **GitHub**: https://github.com/91st1213-blip/chiban-extract
- **PyPI**: https://pypi.org/project/chiban-extract/ (0.1.0 公開済)
- **License**: MIT
- **配布チャネル**: PyPI + GitHub Release

## 利用先

- [[project_real_estate_db]] (J-REIT 所有/取引データ抽出) で実運用予定 (応募時点では未組込)
- [[project_real_estate_db_holdings_complete]] / [[jreit_holdings_extraction]]

## デプロイ・運用

- CI: Python 3.10–3.13 で 56 tests passing
- PyPI publish: 手動 (`python -m build && twine upload`)
- GitHub Release: sdist + wheel 添付

## OSS 応募 (Codex for OSS)

- 応募指示書: `~/Desktop/codex-for-oss-application.md` (Claude for Chrome 用、完成済)
- 応募方針: 速度優先、完璧主義しない (2026-06-14 確定)
- traction 証拠は J-REIT 周りに集中。正直に出す

## 関連ファイル

- [README.md](./README.md) — 使い方
- [CHANGELOG.md](./CHANGELOG.md) — Keep a Changelog 形式
- [CONTRIBUTING.md](./CONTRIBUTING.md) — 開発セットアップ・PR チェックリスト
- [context.md](./context.md) — 直近セッション状況

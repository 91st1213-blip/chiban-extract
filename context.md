# context.md — chiban-extract

直近の作業コンテキスト・進行中タスク・引き継ぎ。

最終更新: 2026-07-04

## 直近の主要マイルストーン

| 日付 | 達成 |
|---|---|
| 2026-06-14 | 0.1.0 PyPI publish + GitHub Release v0.1.0 (sdist+wheel 添付) |
| 2026-06-14 | CHANGELOG / CONTRIBUTING / Issue・PR テンプレ / README badges 整備 |
| 2026-06-14 | 自分名義 (Takumi Sugimoto / 91st1213@gmail.com) のコミット 4 つ追加 (Claude 単独編集問題を緩和) |
| 2026-06-14 | 56 tests passing、CI green (Python 3.10–3.13) |
| 2026-07-04 | ローカル `.claude/settings.json` を追加 (context.md Stop リマインダ hook)。 OSS 公開 repo のため `.claude/` は `.gitignore` に追加、 upstream には出さない (外部 contributor に `~/.claude/hooks/*` を要求しない)。 本体コード変更なし |

## 進行中

### Codex for OSS 応募提出
- 2026-06-14 時点で OpenAI Organization ID が未取得のため延期 → 来週着手予定
- 手順:
  1. https://platform.openai.com/ Settings → Organization → General で `org-xxxx...` 取得
  2. `~/Desktop/codex-for-oss-application.md` を Claude for Chrome に読ませて応募フォーム記入
  3. Stars/DL は正直な数字で記載

## 直近セッションの変更

(セッションごとにここを書き換える)

## 既知の制約 / 前提

- **同一メンテナの他プロジェクトでまだ未組込**: real-estate-db / jreit-holdings-extraction で実運用予定だが、応募時点では traction 証拠としては「予定」止まり
- **Python 3.10+**: 3.10–3.13 で CI 通過。3.14 venv はローカル開発のみ
- **MIT License**: 商用利用可。J-REIT 関連の社内案件にも使える

## 次に着手しうるもの

- OpenAI Organization ID 取得 → 応募提出
- real-estate-db への組込 (現在は ad-hoc 抽出ロジックがリポ内に散在、chiban-extract に置き換え)
- 0.2.0 機能追加 (例: 法人住所抽出、街区符号 / 道路名対応)
- 日本郵便 / e-Stat 標準地域コードとの連携 helper

## 関連ドキュメント

- [project.md](./project.md) — 目的・スコープ・運営方針
- [README.md](./README.md) — 使い方
- [CHANGELOG.md](./CHANGELOG.md)
- [CONTRIBUTING.md](./CONTRIBUTING.md)
- `~/Desktop/codex-for-oss-application.md` — Codex for OSS 応募指示書

# crawler

[![Release](https://img.shields.io/github/v/release/arisakaso/crawler)](https://img.shields.io/github/v/release/arisakaso/crawler)
[![Build status](https://img.shields.io/github/actions/workflow/status/arisakaso/crawler/main.yml?branch=main)](https://github.com/arisakaso/crawler/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/arisakaso/crawler/branch/main/graph/badge.svg)](https://codecov.io/gh/arisakaso/crawler)
[![Commit activity](https://img.shields.io/github/commit-activity/m/arisakaso/crawler)](https://img.shields.io/github/commit-activity/m/arisakaso/crawler)
[![License](https://img.shields.io/github/license/arisakaso/crawler)](https://img.shields.io/github/license/arisakaso/crawler)

crawler

- **Github repository**: <https://github.com/arisakaso/crawler/>
- **Documentation** <https://arisakaso.github.io/crawler/>

## Getting started with your project

### 1. Create a New Repository

First, create a repository on GitHub with the same name as this project, and then run the following commands:

```bash
git init -b main
git add .
git commit -m "init commit"
git remote add origin git@github.com:arisakaso/crawler.git
git push -u origin main
```

### 2. Set Up Your Development Environment

Then, install the environment and the pre-commit hooks with

```bash
make install
```

This will also generate your `uv.lock` file

### 3. Run the pre-commit hooks

Initially, the CI/CD pipeline might be failing due to formatting issues. To resolve those run:

```bash
uv run pre-commit run -a
```

### 4. Commit the changes

Lastly, commit the changes made by the two steps above to your repository.

```bash
git add .
git commit -m 'Fix formatting issues'
git push origin main
```

You are now ready to start development on your project!
The CI/CD pipeline will be triggered when you open a pull request, merge to main, or when you create a new release.

To finalize the set-up for publishing to PyPI, see [here](https://fpgmaas.github.io/cookiecutter-uv/features/publishing/#set-up-for-pypi).
For activating the automatic documentation with MkDocs, see [here](https://fpgmaas.github.io/cookiecutter-uv/features/mkdocs/#enabling-the-documentation-on-github).
To enable the code coverage reports, see [here](https://fpgmaas.github.io/cookiecutter-uv/features/codecov/).

## Releasing a new version



---

Repository initiated with [fpgmaas/cookiecutter-uv](https://github.com/fpgmaas/cookiecutter-uv).

## Gemini（google-genai）を使った抽出の実行方法（最小）

環境変数に Gemini API キーを設定し、対象URLを指定して実行します。
本リポジトリでは `.env.local`（リポジトリルート）を自動読込します。

```bash
# どちらかでOK（.env.local推奨）
# 1) .env.local に GEMINI_API_KEY=... を記載（自動読込）
uv run python -m crawler --url "https://ricohimagingstore.com/Form/Product/ProductDetail.aspx?shop=0&pid=S0001551&cat=002010" --vendor "RICOH 公式"

# 2) 直接環境変数で渡す場合
export GEMINI_API_KEY=YOUR_KEY
uv run python -m crawler --url "https://ricohimagingstore.com/Form/Product/ProductDetail.aspx?shop=0&pid=S0001551&cat=002010" --vendor "RICOH 公式"
```

デフォルトのモデルは `gemini-2.5-flash` です（`GEMINI_MODEL` で上書き可能）。URL Context Tool を使用して指定URLの内容をコンテキストとして渡します。

出力は以下のJSONスキーマ（1オブジェクト）です。

```json
{
  "item": "...",
  "vendor": "RICOH 公式",
  "status": "受付中" | "予定" | "終了",
  "entryStartAt": "2025-09-01T10:00:00+09:00" | null,
  "entryEndAt": "2025-09-10T23:59:00+09:00" | null,
  "lotteryAt": "2025-09-12T12:00:00+09:00" | null,
  "salesStartAt": "2025-09-20T10:00:00+09:00" | null,
  "link": "https://..."
}
```

テスト（GEMINI_API_KEYがあり、かつ google-genai が導入されている場合のみ実行。.env.local も可）

```bash
# .env.local を利用する場合はそのまま
uv run pytest -k gemini_extractor

# 直接渡す場合
export GEMINI_API_KEY=YOUR_KEY
uv run pytest -k gemini_extractor
```

from __future__ import annotations

import json
import os
import re
from typing import Any

from google import genai

from .env import load_env_local


def _ensure_client() -> genai.Client:
    # Load .env.local/.env if present (do not override existing env)
    load_env_local()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError
    return genai.Client(api_key=api_key)


def _build_prompt(url: str, vendor_hint: str | None) -> str:
    vendor_clause = (
        f"ベンダー名は原則『{vendor_hint}』を返してください。該当しなければページやドメインから判断してください。"
        if vendor_hint
        else "ベンダー名はページやドメインから自然に推定してください。"
    )

    return f"""
あなたはEC/販売ページから販売スケジュール情報を抽出するアシスタントです。
次のURLの内容をもとに、以下のJSONスキーマに完全準拠した1オブジェクトを日本語で生成してください。
対象URL: {url}

制約:
- 出力は厳密なJSONのみ(前後に説明やコードフェンスなし)。
- 日付は可能ならISO 8601(例: 2025-09-10T23:59:00+09:00)。不明な場合はnull。
- ステータスは以下のいずれか: "受付中" | "予定" | "終了"。
- ステータスの決め方(おおよそ): 受付終了が過去→"終了"、開始済みかつ未終了→"受付中"、それ以外→"予定"。
- 不確実な場合は予定に寄せてください。
- {vendor_clause}

スキーマ:
{{
  "item": string,             // 商品名
  "vendor": string,           // 販売元名
  "status": "受付中"|"予定"|"終了",
  "entryStartAt": string|null, // 受付開始日
  "entryEndAt": string|null,   // 受付終了日
  "lotteryAt": string|null,    // 抽選発表日
  "salesStartAt": string|null, // 販売開始日
  "link": string              // 対象ページのURL
}}
""".strip()


def _parse_json(text: str) -> dict[str, Any]:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # ```json ... ``` の場合を救出
        m = re.search(r"```json\n(.*?)\n```", text, re.DOTALL | re.IGNORECASE)
        if m:
            return json.loads(m.group(1))
        # 最初の{}を抽出して再挑戦
        m2 = re.search(r"\{[\s\S]*\}", text)
        if m2:
            return json.loads(m2.group(0))
        raise


def _resp_text(resp: Any) -> str:
    # google-genai は response.text を提供。なければ候補から抽出。
    if hasattr(resp, "text") and isinstance(resp.text, str):
        return resp.text  # type: ignore[no-any-return]
    cands = getattr(resp, "candidates", None)
    if cands:
        try:
            parts = getattr(cands[0].content, "parts", [])
            texts = [getattr(p, "text", "") for p in parts if getattr(p, "text", "")]
            if texts:
                return "\n".join(texts)
        except Exception:
            return str(resp)
    return str(resp)


def generate_from_url(url: str, vendor_hint: str | None = None) -> dict[str, Any]:
    client = _ensure_client()
    prompt = _build_prompt(url, vendor_hint)
    model_name = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")

    # URL Context Tool を有効化し、プロンプト内でURLを参照させる
    config = {
        "tools": [{"url_context": {}}],
    }

    resp = client.models.generate_content(model=model_name, contents=[prompt], config=config)

    return _parse_json(_resp_text(resp))

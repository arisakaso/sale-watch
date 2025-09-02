import os

import pytest

from crawler.env import load_env_local

# .env.local / .env を事前に読み込む
load_env_local()

try:
    from google import genai
    from google.genai.types import GenerateContentConfig

    _GENAI_AVAILABLE = True
except Exception:  # pragma: no cover
    _GENAI_AVAILABLE = False


pytestmark = pytest.mark.skipif(
    not (os.environ.get("GEMINI_API_KEY") and _GENAI_AVAILABLE),
    reason="Requires GEMINI_API_KEY and google-genai",
)


def test_gemini_ping():
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])  # type: ignore[name-defined]
    model = os.environ.get("GEMINI_MODEL", "gemini-1.5-flash")

    # 軽量・短時間応答での疎通確認
    try:
        resp = client.models.generate_content(
            model=model, contents="ping", config=GenerateContentConfig(max_output_tokens=16)
        )
    except TypeError:
        # config 非対応の場合
        resp = client.models.generate_content(model=model, contents="ping")

    text = getattr(resp, "text", None) or str(resp)
    assert isinstance(text, str) and len(text) > 0

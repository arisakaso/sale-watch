import os

import pytest
from google import genai

from crawler.env import load_env_local
from crawler.extractor import extract_reservation

TARGET_URL = "https://ricohimagingstore.com/Form/Product/ProductDetail.aspx?shop=0&pid=S0001551&cat=002010"


# まず .env.local/.env を読み込んでからスキップ判定
load_env_local()
pytestmark = pytest.mark.skipif(
    not os.environ.get("GEMINI_API_KEY"),
    reason="Requires GEMINI_API_KEY",
)


def test_gemini_ping():
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])  # type: ignore[name-defined]
    model = os.environ.get("GEMINI_MODEL", "gemini-1.5-flash")

    resp = client.models.generate_content(model=model, contents="ping")
    text = getattr(resp, "text", None) or str(resp)
    assert isinstance(text, str) and len(text) > 0


def test_extract_reservation_live():
    data = extract_reservation(TARGET_URL, vendor_hint="RICOH 公式")
    assert data.item and isinstance(data.item, str)
    assert data.vendor and isinstance(data.vendor, str)
    assert data.status in ("受付中", "予定", "終了")
    assert data.link == TARGET_URL
    # 日付は取得できない場合もあるのでnull許容。取得できた場合は長さで軽く検証。
    for field in ("entryStartAt", "entryEndAt", "lotteryAt", "salesStartAt"):
        v = getattr(data, field)
        if v is not None:
            assert isinstance(v, str)
            assert len(v) >= 10

from __future__ import annotations

from urllib.parse import urlparse

from .gemini_client import generate_from_url
from .models import ExtractedReservation


def _vendor_from_domain(url: str) -> str:
    host = urlparse(url).hostname or ""
    host = host.lower()
    if "ricohimagingstore" in host or "ricoh" in host:
        return "RICOH 公式"
    return host or "Unknown"


def extract_reservation(url: str, vendor_hint: str | None = None) -> ExtractedReservation:
    raw = generate_from_url(url, vendor_hint=vendor_hint)

    # フィールド補完/フォールバック
    if not raw.get("vendor"):
        raw["vendor"] = vendor_hint or _vendor_from_domain(url)
    raw["link"] = raw.get("link") or url

    # Pydanticで検証
    data = ExtractedReservation.model_validate(raw)
    return data

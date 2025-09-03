from __future__ import annotations

from .gemini_client import generate_from_url
from .models import ExtractedReservation


def extract_reservation(url: str, vendor_hint: str | None = None) -> ExtractedReservation:
    raw = generate_from_url(url, vendor_hint=vendor_hint)

    raw["link"] = raw.get("link") or url

    data = ExtractedReservation.model_validate(raw)
    return data

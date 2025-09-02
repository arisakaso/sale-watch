from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, HttpUrl, TypeAdapter, field_validator

ReservationStatus = Literal["受付中", "予定", "終了"]


class ExtractedReservation(BaseModel):
    item: str
    vendor: str
    status: ReservationStatus
    entryStartAt: str | None = None
    entryEndAt: str | None = None
    lotteryAt: str | None = None
    salesStartAt: str | None = None
    link: str

    @field_validator("item", "vendor")
    @classmethod
    def non_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError
        return v.strip()

    @field_validator("link")
    @classmethod
    def valid_link(cls, v: str) -> str:
        # Validate as HttpUrl but store as plain string for TS整合
        TypeAdapter(HttpUrl).validate_python(v)
        return v

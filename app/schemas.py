from __future__ import annotations

from pydantic import BaseModel


class CargoSchema(BaseModel):
    cargo_type: str
    rate: float


class TariffSchema(BaseModel):
    cargo_type: str
    created_at: str
    price: float

"""Схемы: Общее — Рейтинг продавца."""
from pydantic import BaseModel


class SupplierRatingModel(BaseModel):
    """Рейтинг продавца от WB API."""
    feedbackCount: int | None = None
    valuation: float | None = None

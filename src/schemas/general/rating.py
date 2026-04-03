"""Схемы: Общее — Рейтинг продавца."""
from pydantic import BaseModel


class SupplierRatingModel(BaseModel):
    """Рейтинг продавца (GET /api/common/v1/rating)."""
    current: float | None = None
    wbRating: float | None = None
    deliverySpeed: float | None = None
    qualityGoods: float | None = None
    serviceReview: float | None = None

"""Схемы: Общее — Информация о продавце."""
from pydantic import BaseModel


class SellerInfo(BaseModel):
    """Информация о продавце (GET /api/v1/seller-info)."""
    name: str
    sid: str
    tradeMark: str
    itn: str | None = None

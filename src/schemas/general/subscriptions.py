"""Схемы: Общее — Подписки Джем."""
from pydantic import BaseModel


class SubscriptionsJamInfo(BaseModel):
    """Информация о подписке Джем (GET /api/common/v1/subscriptions)."""
    since: str | None = None
    till: str | None = None
    tariff: str | None = None
    isActive: bool | None = None

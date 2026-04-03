"""Схемы: Общее — Подписки Джем."""
from pydantic import BaseModel


class SubscriptionsJamInfo(BaseModel):
    """Информация о подписке Джем от WB API."""
    state: str | None = None              # active | inactive
    activationSource: str | None = None   # constructor | jam
    level: str | None = None              # standard | advanced | premium
    since: str | None = None              # ISO 8601 datetime
    till: str | None = None               # ISO 8601 datetime

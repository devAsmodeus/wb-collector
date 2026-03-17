"""Схемы: Аналитика — Воронка продаж."""
from pydantic import BaseModel, Field


class FunnelProductsRequest(BaseModel):
    """Запрос воронки продаж по товарам."""
    nmIDs: list[int] | None = Field(None, description="Артикулы WB (nmID). Максимум 20.")
    startDate: str = Field(description="Дата начала периода в формате `YYYY-MM-DD`")
    endDate: str = Field(description="Дата окончания периода в формате `YYYY-MM-DD`")
    brandNames: list[str] | None = Field(None, description="Фильтр по брендам")
    objectIDs: list[int] | None = Field(None, description="Фильтр по предметам")
    tagIDs: list[int] | None = Field(None, description="Фильтр по тегам")
    timezone: str | None = Field(None, description="Временная зона. По умолчанию: Europe/Moscow")
    aggregationLevel: str | None = Field(None, description="Уровень агрегации: `day`, `week`, `month`")


class FunnelHistoryRequest(BaseModel):
    """Запрос истории воронки продаж."""
    nmIDs: list[int] | None = Field(None, description="Артикулы WB (nmID). Максимум 20.")
    startDate: str = Field(description="Дата начала периода в формате `YYYY-MM-DD`")
    endDate: str = Field(description="Дата окончания периода в формате `YYYY-MM-DD`")
    brandNames: list[str] | None = Field(None, description="Фильтр по брендам")
    objectIDs: list[int] | None = Field(None, description="Фильтр по предметам")
    tagIDs: list[int] | None = Field(None, description="Фильтр по тегам")
    timezone: str | None = Field(None, description="Временная зона. По умолчанию: Europe/Moscow")
    aggregationLevel: str | None = Field(None, description="Уровень агрегации: `day`, `week`, `month`")


class FunnelGroupedHistoryRequest(BaseModel):
    """Запрос сгруппированной истории воронки."""
    startDate: str = Field(description="Дата начала периода в формате `YYYY-MM-DD`")
    endDate: str = Field(description="Дата окончания периода в формате `YYYY-MM-DD`")
    brandNames: list[str] | None = Field(None, description="Фильтр по брендам")
    objectIDs: list[int] | None = Field(None, description="Фильтр по предметам")
    tagIDs: list[int] | None = Field(None, description="Фильтр по тегам")
    timezone: str | None = Field(None, description="Временная зона. По умолчанию: Europe/Moscow")
    aggregationLevel: str | None = Field(None, description="Уровень агрегации: `day`, `week`, `month`")
    dimension: str | None = Field(None, description="Группировка: `brand`, `object`, `tag`")

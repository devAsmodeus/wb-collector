"""Схемы: Аналитика — История остатков."""
from pydantic import BaseModel, Field


class StocksGroupsRequest(BaseModel):
    """Запрос остатков по группам товаров."""
    startDate: str = Field(description="Дата начала периода в формате `YYYY-MM-DD`")
    endDate: str = Field(description="Дата окончания периода в формате `YYYY-MM-DD`")
    nmIDs: list[int] | None = Field(None, description="Артикулы WB (nmID)")
    brandNames: list[str] | None = Field(None, description="Фильтр по брендам")
    objectIDs: list[int] | None = Field(None, description="Фильтр по предметам")
    tagIDs: list[int] | None = Field(None, description="Фильтр по тегам")
    timezone: str | None = Field(None, description="Временная зона. По умолчанию: Europe/Moscow")
    aggregationLevel: str | None = Field(None, description="Уровень агрегации: `day`, `week`, `month`")


class StocksProductsRequest(BaseModel):
    """Запрос остатков по артикулам."""
    startDate: str = Field(description="Дата начала периода в формате `YYYY-MM-DD`")
    endDate: str = Field(description="Дата окончания периода в формате `YYYY-MM-DD`")
    nmIDs: list[int] | None = Field(None, description="Артикулы WB (nmID). Максимум 20.")
    brandNames: list[str] | None = Field(None, description="Фильтр по брендам")
    objectIDs: list[int] | None = Field(None, description="Фильтр по предметам")
    tagIDs: list[int] | None = Field(None, description="Фильтр по тегам")
    timezone: str | None = Field(None, description="Временная зона. По умолчанию: Europe/Moscow")
    aggregationLevel: str | None = Field(None, description="Уровень агрегации: `day`, `week`, `month`")
    limit: int | None = Field(None, description="Количество записей на странице")
    offset: int | None = Field(None, description="Смещение для пагинации")


class StocksSizesRequest(BaseModel):
    """Запрос остатков по размерам."""
    startDate: str = Field(description="Дата начала периода в формате `YYYY-MM-DD`")
    endDate: str = Field(description="Дата окончания периода в формате `YYYY-MM-DD`")
    nmID: int = Field(description="Артикул WB (nmID)")
    timezone: str | None = Field(None, description="Временная зона. По умолчанию: Europe/Moscow")
    aggregationLevel: str | None = Field(None, description="Уровень агрегации: `day`, `week`, `month`")
    limit: int | None = Field(None, description="Количество записей")
    offset: int | None = Field(None, description="Смещение")


class StocksOfficesRequest(BaseModel):
    """Запрос остатков по складам."""
    startDate: str = Field(description="Дата начала периода в формате `YYYY-MM-DD`")
    endDate: str = Field(description="Дата окончания периода в формате `YYYY-MM-DD`")
    nmIDs: list[int] | None = Field(None, description="Артикулы WB (nmID). Максимум 20.")
    brandNames: list[str] | None = Field(None, description="Фильтр по брендам")
    objectIDs: list[int] | None = Field(None, description="Фильтр по предметам")
    tagIDs: list[int] | None = Field(None, description="Фильтр по тегам")
    officeIDs: list[int] | None = Field(None, description="Фильтр по складам WB")
    timezone: str | None = Field(None, description="Временная зона. По умолчанию: Europe/Moscow")
    aggregationLevel: str | None = Field(None, description="Уровень агрегации: `day`, `week`, `month`")

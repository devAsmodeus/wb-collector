"""Схемы: Аналитика — Поисковые запросы по товарам."""
from pydantic import BaseModel, Field


class SearchReportRequest(BaseModel):
    """Запрос отчёта по поисковым запросам."""
    startDate: str = Field(description="Дата начала периода в формате `YYYY-MM-DD`")
    endDate: str = Field(description="Дата окончания периода в формате `YYYY-MM-DD`")
    nmIDs: list[int] | None = Field(None, description="Артикулы WB (nmID)")
    brandNames: list[str] | None = Field(None, description="Фильтр по брендам")
    objectIDs: list[int] | None = Field(None, description="Фильтр по предметам")
    tagIDs: list[int] | None = Field(None, description="Фильтр по тегам")
    timezone: str | None = Field(None, description="Временная зона. По умолчанию: Europe/Moscow")
    limit: int | None = Field(None, description="Количество записей на странице")
    offset: int | None = Field(None, description="Смещение для пагинации")


class SearchGroupsRequest(BaseModel):
    """Запрос сгруппированных поисковых запросов."""
    startDate: str = Field(description="Дата начала периода в формате `YYYY-MM-DD`")
    endDate: str = Field(description="Дата окончания периода в формате `YYYY-MM-DD`")
    nmIDs: list[int] | None = Field(None, description="Артикулы WB (nmID)")
    brandNames: list[str] | None = Field(None, description="Фильтр по брендам")
    objectIDs: list[int] | None = Field(None, description="Фильтр по предметам")
    tagIDs: list[int] | None = Field(None, description="Фильтр по тегам")
    timezone: str | None = Field(None, description="Временная зона. По умолчанию: Europe/Moscow")


class SearchTextsRequest(BaseModel):
    """Запрос поисковых текстов по товару."""
    startDate: str = Field(description="Дата начала периода в формате `YYYY-MM-DD`")
    endDate: str = Field(description="Дата окончания периода в формате `YYYY-MM-DD`")
    nmID: int = Field(description="Артикул WB (nmID)")
    timezone: str | None = Field(None, description="Временная зона. По умолчанию: Europe/Moscow")
    limit: int | None = Field(None, description="Количество записей")
    offset: int | None = Field(None, description="Смещение")


class SearchOrdersRequest(BaseModel):
    """Запрос заказов из поиска по товару."""
    startDate: str = Field(description="Дата начала периода в формате `YYYY-MM-DD`")
    endDate: str = Field(description="Дата окончания периода в формате `YYYY-MM-DD`")
    nmID: int = Field(description="Артикул WB (nmID)")
    timezone: str | None = Field(None, description="Временная зона. По умолчанию: Europe/Moscow")
    limit: int | None = Field(None, description="Количество записей")
    offset: int | None = Field(None, description="Смещение")

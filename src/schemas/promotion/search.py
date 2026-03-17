"""Схемы: Маркетинг — Поисковые кластеры (нормальные запросы)."""
from pydantic import BaseModel, Field


class NormQueryStatsRequest(BaseModel):
    """Запрос статистики поисковых кластеров."""
    from_: str = Field(alias="from", description="Дата начала периода в формате `YYYY-MM-DD`")
    to: str = Field(description="Дата окончания периода в формате `YYYY-MM-DD`")
    items: list[dict] = Field(description="Список кампаний и кластеров для получения статистики")

    model_config = {"populate_by_name": True}


class NormQueryGetBidsRequest(BaseModel):
    """Запрос ставок по поисковым кластерам."""
    items: list[dict] = Field(description="Кампании и кластеры, по которым нужны ставки")


class NormQueryBid(BaseModel):
    """Ставка по поисковому кластеру."""
    advert_id: int = Field(description="ID кампании")
    cluster_id: int = Field(description="ID кластера")
    bid: int = Field(description="Ставка, руб.")


class NormQuerySetBidsRequest(BaseModel):
    """Установка/удаление ставок по поисковым кластерам."""
    bids: list[NormQueryBid] = Field(description="Ставки по кластерам")


class NormQueryGetMinusRequest(BaseModel):
    """Запрос минус-слов по поисковым кластерам."""
    items: list[dict] = Field(description="Кампании и кластеры для получения минус-слов")


class NormQuerySetMinusRequest(BaseModel):
    """Установка минус-слов по поисковому кластеру."""
    advert_id: int = Field(description="ID кампании")
    nm_id: int = Field(description="Артикул WB (nmID)")
    norm_queries: list[str] = Field(description="Список поисковых запросов для добавления в минус-слова")


class NormQueryListRequest(BaseModel):
    """Получение списка поисковых кластеров."""
    items: list[dict] = Field(description="Кампании и артикулы для получения кластеров")


class NormQueryStatsV1Request(BaseModel):
    """Запрос статистики поисковых кластеров (v1)."""
    from_: str = Field(alias="from", description="Дата начала периода в формате `YYYY-MM-DD`")
    to: str = Field(description="Дата окончания периода в формате `YYYY-MM-DD`")
    items: list[dict] = Field(description="Список кампаний и кластеров")

    model_config = {"populate_by_name": True}

"""Схемы: Маркетинг — Статистика и медиакампании."""
from pydantic import BaseModel, Field


class FullStatsResponse(BaseModel):
    """Полная статистика по кампаниям."""
    data: list[dict] | None = Field(None, description="Статистика по кампаниям за период")


class CampaignStatsRequest(BaseModel):
    """Запрос статистики кампаний (детализированной)."""
    intervals: list[dict] = Field(
        description="Список объектов с полями `id` (ID кампании) и интервалом дат"
    )


class MediaCampaignCountResponse(BaseModel):
    """Количество медиакампаний."""
    all: int | None = Field(None, description="Общее количество медиакампаний всех статусов и типов")
    adverts: dict | None = Field(None, description="Количество по типам и статусам")


class MediaCampaignItem(BaseModel):
    """Медиакампания."""
    advertId: int | None = Field(None, description="ID медиакампании")
    name: str | None = Field(None, description="Название медиакампании")
    brand: str | None = Field(None, description="Название бренда")
    type: int | None = Field(
        None,
        description="Тип: `1` — размещение по дням, `2` — по просмотрам",
    )
    status: int | None = Field(
        None,
        description="Статус: `1` — черновик, `2` — модерация, `3` — отклонена, `4` — активна, `5` — завершена",
    )
    createTime: str | None = Field(None, description="Время создания (ISO 8601)")
    extended: dict | None = Field(None, description="Расширенные данные медиакампании")
    items: list[dict] | None = Field(None, description="Информация о баннерах")


class MediaCampaignsResponse(BaseModel):
    """Список медиакампаний."""
    adverts: list[MediaCampaignItem] = Field(default=[], description="Медиакампании")


class NmsRequest(BaseModel):
    """Запрос артикулов для создания кампаний."""
    nms: list[int] = Field(description="Список артикулов WB (nmID)")

"""Схемы: Маркетинг — Кампании и управление."""
from pydantic import BaseModel, Field


class AdvertCountItem(BaseModel):
    """Количество кампаний по статусу."""
    status: int | None = Field(None, description="Статус кампании")
    count: int | None = Field(None, description="Количество кампаний в данном статусе")


class AdvertCountResponse(BaseModel):
    """Количество кампаний по типам и статусам."""
    adverts: list[AdvertCountItem] | None = Field(None, description="Данные по кампаниям")
    all: int | None = Field(None, description="Общее количество кампаний всех статусов и типов")


class AdvertInfo(BaseModel):
    """Информация о рекламной кампании."""
    advertId: int | None = Field(None, description="ID кампании")
    name: str | None = Field(None, description="Название кампании")
    status: int | None = Field(
        None,
        description=(
            "Статус кампании:\n"
            "- `-1` — удалена\n- `4` — готова к запуску\n"
            "- `7` — завершена\n- `8` — отказ\n- `9` — идут показы\n- `11` — на паузе"
        ),
    )
    type: int | None = Field(
        None,
        description="Тип кампании: `4` — каталог, `5` — карточка, `6` — поиск, `7` — рекомендации, `9` — авто",
    )
    paymentType: str | None = Field(None, description="Тип оплаты: `cpm` — за показы, `cpc` — за клики")
    createTime: str | None = Field(None, description="Дата и время создания кампании (ISO 8601)")
    changeTime: str | None = Field(None, description="Дата и время последнего изменения (ISO 8601)")
    startTime: str | None = Field(None, description="Дата и время запуска кампании (ISO 8601)")
    endTime: str | None = Field(None, description="Дата и время завершения кампании (ISO 8601)")


class AdvertsResponse(BaseModel):
    """Список рекламных кампаний."""
    adverts: list[AdvertInfo] = Field(default=[], description="Рекламные кампании")


class MinBidRequest(BaseModel):
    """Запрос минимальных ставок."""
    advert_id: int = Field(description="ID кампании")
    nm_ids: list[int] = Field(description="Список артикулов WB (nmID)")
    payment_type: str = Field(description="Тип оплаты: `cpm` — за показы, `cpc` — за клики")
    placement_types: list[str] = Field(
        description="Места размещения: `search` — поиск, `recommendation` — рекомендации",
    )


class CreateCampaignRequest(BaseModel):
    """Создание рекламной кампании."""
    name: str = Field(description="Название кампании (максимум 100 символов)")
    nms: list[int] = Field(description="Артикулы WB (nmID) для кампании")
    bid_type: str = Field(description="Тип ставки: `manual` — ручная, `unified` — единая")
    payment_type: str = Field(description="Тип оплаты: `cpm` — за показы, `cpc` — за клики")
    placement_types: list[str] = Field(
        description="Места размещения: `search` — в поиске, `recommendations` — в рекомендациях",
    )


class RenameRequest(BaseModel):
    """Переименование кампании."""
    advertId: int = Field(description="ID кампании")
    name: str = Field(description="Новое название кампании (максимум 100 символов)")


class UpdatePlacementsRequest(BaseModel):
    """Обновление мест размещения в кампаниях."""
    placements: list[dict] = Field(description="Места размещения в кампаниях")


class UpdateBidsRequest(BaseModel):
    """Обновление ставок в кампаниях."""
    bids: list[dict] = Field(description="Ставки в кампаниях")


class UpdateNmsRequest(BaseModel):
    """Обновление артикулов в кампаниях."""
    nms: list[dict] = Field(description="Карточки товаров в кампаниях")


class SubjectsResponse(BaseModel):
    """Предметы для рекламных кампаний."""
    subjects: list[dict] = Field(default=[], description="Доступные предметы для создания кампании")


class BidRecommendation(BaseModel):
    """Рекомендация по ставке."""
    advertId: int | None = Field(None, description="ID кампании")
    nmId: int | None = Field(None, description="Артикул WB")
    position: int | None = Field(None, description="Рекомендуемая позиция")
    bid: int | None = Field(None, description="Рекомендуемая ставка, руб.")

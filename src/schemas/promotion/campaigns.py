"""Схемы: Маркетинг — Кампании и управление."""
from pydantic import BaseModel, Field


class AdvertListItem(BaseModel):
    """Элемент advert_list (advertId + changeTime) из /adv/v1/promotion/count."""
    advertId: int | None = Field(None)
    changeTime: str | None = Field(None)


class AdvertCountItem(BaseModel):
    """Группа кампаний по типу и статусу."""
    type: int | None = Field(None)
    status: int | None = Field(None)
    count: int | None = Field(None)
    advert_list: list[AdvertListItem] | None = Field(None)


class AdvertCountResponse(BaseModel):
    """Количество кампаний по типам и статусам."""
    adverts: list[AdvertCountItem] | None = Field(None)
    all: int | None = Field(None)


class AdvertInfo(BaseModel):
    """Информация об отдельной кампании."""
    advertId: int | None = Field(None)
    name: str | None = Field(None)
    status: int | None = Field(None)
    type: int | None = Field(None)
    paymentType: str | None = Field(None)
    createTime: str | None = Field(None)
    changeTime: str | None = Field(None)
    startTime: str | None = Field(None)
    endTime: str | None = Field(None)


class AdvertsResponse(BaseModel):
    """Список рекламных кампаний."""
    adverts: list[AdvertInfo] = Field(default=[])


class MinBidRequest(BaseModel):
    """Запрос минимальных ставок."""
    advert_id: int = Field(description="ID кампании")
    nm_ids: list[int] = Field(description="Список артикулов WB (nmID)")
    payment_type: str = Field(description="Тип оплаты: `cpm` или `cpc`")
    placement_types: list[str] = Field(description="Типы размещения: `search`, `recommendation`")


class CreateCampaignRequest(BaseModel):
    """Создание рекламной кампании."""
    name: str = Field(description="Название кампании")
    nms: list[int] = Field(description="Артикулы WB (nmID)")
    bid_type: str = Field(description="Тип ставки: `manual` или `unified`")
    payment_type: str = Field(description="Тип оплаты: `cpm` или `cpc`")
    placement_types: list[str] = Field(description="Типы размещения")


class RenameRequest(BaseModel):
    """Переименование кампании."""
    advertId: int = Field(description="ID кампании")
    name: str = Field(description="Новое название кампании")


class UpdatePlacementsRequest(BaseModel):
    """Обновление мест размещения в кампаниях."""
    placements: list[dict] = Field(description="Места размещения в кампаниях")


class UpdateBidsRequest(BaseModel):
    """Обновление ставок в кампаниях."""
    bids: list[dict] = Field(description="Ставки в кампаниях")


class UpdateNmsRequest(BaseModel):
    """Обновление артикулов в кампаниях."""
    nms: list[dict] = Field(description="Артикулы товаров в кампаниях")


class SubjectsResponse(BaseModel):
    """Предметы для рекламных кампаний."""
    subjects: list[dict] = Field(default=[])


class BidRecommendation(BaseModel):
    """Рекомендация по ставке."""
    advertId: int | None = Field(None)
    nmId: int | None = Field(None)
    position: int | None = Field(None)
    bid: int | None = Field(None)

"""Схемы: Маркетинг — Календарь акций."""
from pydantic import BaseModel, Field


class Promotion(BaseModel):
    """Акция WB."""
    id: int | None = Field(None, description="ID акции")
    name: str | None = Field(None, description="Название акции")
    startDate: str | None = Field(None, description="Дата начала акции (ISO 8601)")
    endDate: str | None = Field(None, description="Дата окончания акции (ISO 8601)")
    type: str | None = Field(None, description="Тип акции")
    inAction: bool | None = Field(None, description="Участвует ли продавец в акции")


class PromotionsResponse(BaseModel):
    """Список акций из календаря."""
    promotions: list[Promotion] = Field(default=[], description="Акции WB")


class PromotionDetails(BaseModel):
    """Детали акции."""
    id: int | None = Field(None, description="ID акции")
    name: str | None = Field(None, description="Название акции")
    description: str | None = Field(None, description="Описание акции")
    startDate: str | None = Field(None, description="Дата начала (ISO 8601)")
    endDate: str | None = Field(None, description="Дата окончания (ISO 8601)")
    conditions: str | None = Field(None, description="Условия участия в акции")


class PromotionNomenclature(BaseModel):
    """Номенклатура (товар) для участия в акции."""
    nmId: int | None = Field(None, description="Артикул WB (nmID)")
    name: str | None = Field(None, description="Наименование товара")
    inAction: bool | None = Field(None, description="Участвует ли товар в акции")
    price: float | None = Field(None, description="Текущая цена, руб.")
    actionPrice: float | None = Field(None, description="Акционная цена, руб.")


class PromotionNomenclaturesResponse(BaseModel):
    """Товары для участия в акции."""
    nomenclatures: list[PromotionNomenclature] = Field(default=[], description="Товары акции")


class UploadPromotionNomenclaturesRequest(BaseModel):
    """Загрузка товаров в акцию."""
    data: list[dict] = Field(description="Список товаров с акционными ценами для загрузки в акцию")

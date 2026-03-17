"""Схемы: Отчёты — Удержания, антифрод, маркировка."""
from pydantic import BaseModel, Field


class MeasurementPenaltyItem(BaseModel):
    """Штраф за некорректные замеры."""
    date: str | None = Field(None, description="Дата штрафа (ISO 8601)")
    officeId: int | None = Field(None, description="ID склада")
    officeName: str | None = Field(None, description="Название склада")
    amount: float | None = Field(None, description="Сумма штрафа, руб.")
    nmId: int | None = Field(None, description="Артикул WB (nmID)")


class WarehouseMeasurementItem(BaseModel):
    """Данные обмера на складе."""
    date: str | None = Field(None, description="Дата обмера (ISO 8601)")
    officeId: int | None = Field(None, description="ID склада")
    officeName: str | None = Field(None, description="Название склада")
    nmId: int | None = Field(None, description="Артикул WB (nmID)")
    vendorCode: str | None = Field(None, description="Артикул продавца")
    measuredVolume: float | None = Field(None, description="Измеренный объём, л")
    declaredVolume: float | None = Field(None, description="Заявленный объём, л")


class DeductionItem(BaseModel):
    """Удержание."""
    date: str | None = Field(None, description="Дата удержания (ISO 8601)")
    type: str | None = Field(None, description="Тип удержания")
    description: str | None = Field(None, description="Описание удержания")
    amount: float | None = Field(None, description="Сумма удержания, руб.")
    nmId: int | None = Field(None, description="Артикул WB (nmID)")


class AntifraudDetailsResponse(BaseModel):
    """Детализация антифрод-удержаний."""
    data: list[dict] | None = Field(None, description="Список удержаний по антифроду")


class GoodsLabelingResponse(BaseModel):
    """Отчёт по маркированным товарам."""
    data: list[dict] | None = Field(None, description="Товары с обязательной маркировкой")

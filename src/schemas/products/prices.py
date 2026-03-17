"""Схемы: Товары — Цены и скидки."""
from typing import Any
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Товары с ценами
# ---------------------------------------------------------------------------

class GoodsSize(BaseModel):
    """Размер товара с ценой."""
    chrtID: int | None = Field(None, description="ID характеристики размера (chrtID)")
    sizeID: int | None = Field(None, description="ID размера (sizeID) — альтернатива chrtID")
    techSize: str | None = Field(None, description="Технический размер (напр. '42', 'XL')")
    techSizeName: str | None = Field(None, description="Отображаемое название размера")
    skus: list[str] = Field(default=[], description="Баркоды (EAN-13) данного размера")
    price: int | None = Field(
        None,
        description="Цена до скидки в копейках × 100 (напр. 300000 = 3000 ₽)",
    )
    discountedPrice: int | None = Field(
        None,
        description="Цена после скидки продавца в копейках × 100",
    )
    clubDiscountedPrice: int | None = Field(
        None,
        description="Цена для участников WB Клуба в копейках × 100",
    )


class GoodsItem(BaseModel):
    """Товар с ценами по размерам."""
    nmID: int = Field(description="Артикул WB (nmID)")
    vendorCode: str = Field(default="", description="Артикул продавца")
    sizes: list[GoodsSize] = Field(default=[], description="Размеры с ценами")
    currencyIsoCode4217: str = Field(default="RUB", description="Валюта цен (ISO 4217, напр. 'RUB')")
    discount: int = Field(default=0, description="Скидка продавца, % (0–95)")
    clubDiscount: int = Field(default=0, description="Скидка WB Клуба, %")
    editableSizePrice: bool = Field(
        default=False,
        description="Если `true` — цену можно устанавливать отдельно для каждого размера",
    )


class GoodsListData(BaseModel):
    listGoods: list[GoodsItem] = Field(default=[], description="Список товаров с ценами")


class GoodsListResponse(BaseModel):
    """Ответ со списком товаров и их ценами."""
    data: GoodsListData | None = Field(None, description="Данные товаров")
    error: bool = Field(default=False, description="Признак ошибки")
    errorText: str = Field(default="", description="Текст ошибки")


# ---------------------------------------------------------------------------
# История загрузок цен
# ---------------------------------------------------------------------------

class PriceHistoryTask(BaseModel):
    """Задача загрузки цен (батч-обновление)."""
    uploadID: int | None = Field(None, description="ID загрузки (задачи обновления цен)")
    status: str | None = Field(
        None,
        description=(
            "Статус загрузки: "
            "`1` — в обработке, "
            "`2` — выполнена, "
            "`3` — ошибка."
        ),
    )
    uploadDate: str | None = Field(None, description="Дата создания задачи (ISO 8601)")
    activationDate: str | None = Field(
        None,
        description="Дата активации (вступления цен в силу). ISO 8601.",
    )


class PriceHistoryResponse(BaseModel):
    """Ответ с историей загрузок цен."""
    data: list[PriceHistoryTask] | Any = Field(None, description="Список задач обновления цен")
    error: bool = Field(default=False, description="Признак ошибки")
    errorText: str = Field(default="", description="Текст ошибки")


# ---------------------------------------------------------------------------
# Товары конкретной загрузки
# ---------------------------------------------------------------------------

class UploadGoodsItem(BaseModel):
    """Товар из батч-загрузки цен."""
    nmID: int = Field(description="Артикул WB")
    vendorCode: str = Field(default="", description="Артикул продавца")
    status: str | None = Field(
        None,
        description="Статус обработки товара в загрузке: `success`, `error`.",
    )
    errorText: str | None = Field(None, description="Текст ошибки (если статус error)")
    price: int | None = Field(None, description="Установленная цена в копейках × 100")
    discount: int | None = Field(None, description="Установленная скидка, %")


class UploadGoodsData(BaseModel):
    listGoods: list[UploadGoodsItem] = Field(default=[], description="Товары загрузки")


class UploadGoodsResponse(BaseModel):
    """Ответ с товарами конкретной задачи загрузки цен."""
    data: UploadGoodsData | Any = Field(None, description="Данные товаров загрузки")
    error: bool = Field(default=False, description="Признак ошибки")
    errorText: str = Field(default="", description="Текст ошибки")


# ---------------------------------------------------------------------------
# Карантин цен
# ---------------------------------------------------------------------------

class QuarantineItem(BaseModel):
    """Товар на карантине цен."""
    nmID: int = Field(description="Артикул WB")
    vendorCode: str = Field(default="", description="Артикул продавца")
    price: int | None = Field(None, description="Текущая цена в копейках × 100")
    discount: int | None = Field(None, description="Текущая скидка, %")
    quarantineReason: str | None = Field(
        None,
        description=(
            "Причина карантина: "
            "`priceIncreased` — цена выросла более чем на 50%, "
            "`priceDecreased` — цена снизилась более чем на 50%."
        ),
    )


class QuarantineData(BaseModel):
    listGoods: list[QuarantineItem] = Field(default=[], description="Товары на карантине")


class QuarantineResponse(BaseModel):
    """Ответ со списком товаров на карантине цен."""
    data: QuarantineData | Any = Field(None, description="Данные карантина")
    error: bool = Field(default=False, description="Признак ошибки")
    errorText: str = Field(default="", description="Текст ошибки")

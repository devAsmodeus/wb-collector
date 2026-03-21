"""Схемы: FBS — Поставки и короба."""
from pydantic import BaseModel, Field


class Supply(BaseModel):
    """Поставка FBS."""
    supplyId: str | None = Field(None, description="ID поставки (напр. `WB-GI-12345678`)")
    name: str | None = Field(None, description="Название поставки")
    closedAt: str | None = Field(None, description="Дата закрытия поставки (ISO 8601)")
    scanDt: str | None = Field(None, description="Дата и время скана поставки на складе WB (ISO 8601)")
    createdAt: str | None = Field(None, description="Дата создания поставки (ISO 8601)")
    isLargeCargo: bool = Field(default=False, description="Является ли поставка крупногабаритной (КГТ)")
    isB2b: bool | None = Field(None, description="Признак B2B-продажи: `true` — B2B, `false` — не B2B, `null` — нет заданий")


class SuppliesResponse(BaseModel):
    """Список поставок."""
    supplies: list[Supply] = Field(default=[], description="Поставки продавца")


class CreateSupplyRequest(BaseModel):
    """Создание новой поставки."""
    name: str = Field(description="Название поставки (произвольное, для удобства идентификации)")


class CreateSupplyResponse(BaseModel):
    """Ответ на создание поставки."""
    id: str = Field(description="ID созданной поставки (напр. `WB-GI-12345678`)")


class SupplyOrder(BaseModel):
    """Сборочное задание в составе поставки."""
    orderId: int | None = Field(None, description="ID сборочного задания")
    article: str | None = Field(None, description="Артикул продавца")
    createdAt: str | None = Field(None, description="Дата создания заказа (ISO 8601)")
    convertedPrice: float | None = Field(None, description="Цена в валюте расчётов")
    currencyCode: int | None = Field(None, description="Числовой код валюты (ISO 4217)")
    nmId: int | None = Field(None, description="Артикул WB (nmID)")
    chrtId: int | None = Field(None, description="ID характеристики размера")
    price: float | None = Field(None, description="Цена, коп×100")
    quantity: int | None = Field(None, description="Количество единиц")
    subject: str | None = Field(None, description="Предмет товара")
    category: str | None = Field(None, description="Категория товара")
    name: str | None = Field(None, description="Наименование товара")
    brand: str | None = Field(None, description="Бренд товара")
    techSize: str | None = Field(None, description="Технический размер")
    skus: list[str] = Field(default=[], description="Баркоды товара")
    wbWhId: int | None = Field(None, description="ID склада WB")


class SupplyOrdersResponse(BaseModel):
    """Заказы в составе поставки."""
    orders: list[SupplyOrder] = Field(default=[], description="Сборочные задания поставки")


class SupplyOrderIdsResponse(BaseModel):
    """ID заказов поставки."""
    orderIds: list[int] = Field(default=[], description="Список ID сборочных заданий в поставке")


class AddOrdersToSupplyRequest(BaseModel):
    """Добавление заказов в поставку."""
    orders: list[int] = Field(
        description="Список ID сборочных заданий для добавления в поставку. Максимум 500 за запрос.",
        max_length=500,
    )


class SupplyBarcode(BaseModel):
    """QR-код поставки для сканирования на складе WB."""
    file: str | None = Field(None, description="QR-код в формате base64")
    type: str | None = Field(None, description="Формат: `svg` или `zplLabel`")


class Box(BaseModel):
    """Короб в составе поставки."""
    id: str = Field(description="ID короба (напр. `WB-TRBX-12345678`)")


class BoxesResponse(BaseModel):
    """Короба поставки."""
    trbx: list[Box] = Field(default=[], description="Список коробов поставки")


class AddBoxesRequest(BaseModel):
    """Добавление коробов к поставке."""
    quantity: int = Field(
        description="Количество коробов для добавления. Диапазон: 1–10 000.",
        ge=1,
        le=10000,
    )


class DeleteBoxesRequest(BaseModel):
    """Удаление коробов из поставки."""
    trbx: list[str] = Field(description="Список ID коробов для удаления (напр. `['WB-TRBX-123', 'WB-TRBX-456']`)")


class BoxStickersRequest(BaseModel):
    """Запрос стикеров для коробов."""
    trbx: list[str] = Field(description="Список ID коробов, для которых нужны стикеры")


class BoxSticker(BaseModel):
    """Стикер для короба."""
    boxId: str | None = Field(None, description="ID короба")
    sticker: str | None = Field(None, description="Стикер в формате base64")


class BoxStickersResponse(BaseModel):
    """Стикеры для коробов поставки."""
    stickers: list[BoxSticker] = Field(default=[], description="Стикеры для печати и наклейки на короба")

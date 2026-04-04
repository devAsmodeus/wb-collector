"""Схемы: FBS — Сборочные задания.

Строго по схеме WB API v3: GET/POST marketplace-api.wildberries.ru/api/v3/orders
Схема Order из 03-orders-fbs.yaml.
"""
from typing import Any
from pydantic import BaseModel, Field


class Order(BaseModel):
    """Сборочное задание FBS (Order schema из YAML)."""
    id: int | None = Field(None, description="id — ID сборочного задания (int64)")
    orderUid: str | None = Field(None, description="orderUid — UUID заказа")
    rid: str | None = Field(None, description="rid — уникальный ID позиции заказа")
    createdAt: str | None = Field(None, description="createdAt — дата создания (ISO 8601)")
    article: str | None = Field(None, description="article — артикул продавца")
    colorCode: str | None = Field(None, description="colorCode — код цвета")
    nmId: int | None = Field(None, description="nmId — артикул WB")
    chrtId: int | None = Field(None, description="chrtId — ID характеристики размера")
    price: int | None = Field(None, description="price — цена в копейках × 100")
    convertedPrice: int | None = Field(None, description="convertedPrice — цена в валюте продавца")
    currencyCode: int | None = Field(None, description="currencyCode — код валюты ISO 4217")
    convertedCurrencyCode: int | None = Field(None, description="convertedCurrencyCode")
    deliveryType: str | None = Field(None, description="deliveryType — тип доставки (fbs/dbs/wbexpress)")
    supplyId: str | None = Field(None, description="supplyId — ID поставки FBS")
    warehouseId: int | None = Field(None, description="warehouseId — ID склада продавца")
    officeId: int | None = Field(None, description="officeId — ID офиса WB (ПВЗ)")
    cargoType: int | None = Field(None, description="cargoType — тип груза (1=короба, 2=паллеты, 3=суперсейф)")
    crossBorderType: int | None = Field(None, description="crossBorderType — тип кроссбордер")
    scanPrice: float | None = Field(None, description="scanPrice — цена при сканировании (uint32)")
    isZeroOrder: bool = Field(default=False, description="isZeroOrder — нулевой заказ")
    comment: str | None = Field(None, description="comment — комментарий к заказу")
    skus: list[str] | None = Field(None, description="skus — баркоды товара")
    offices: list[str] | None = Field(None, description="offices — коды офисов доставки")
    address: dict | Any = Field(None, description="address — объект адреса доставки")
    options: dict | Any = Field(None, description="options — доп. опции (isB2B и др.)")

    model_config = {"extra": "allow"}


class OrdersResponse(BaseModel):
    """Ответ GET /api/v3/orders."""
    orders: list[Order] = Field(default=[], description="Список сборочных заданий")
    next: int | None = Field(None, description="Курсор для следующей страницы (next)")


class OrderStatusInfo(BaseModel):
    """Статус конкретного заказа."""
    id: int = Field(description="ID заказа")
    supplierStatus: str | None = Field(None, description="Статус у продавца")
    wbStatus: str | None = Field(None, description="Статус WB")


class OrderStatusResponse(BaseModel):
    """Ответ POST /api/v3/orders/status."""
    orders: list[OrderStatusInfo] = Field(default=[])


class StickerItem(BaseModel):
    """Стикер для сборочного задания."""
    orderId: int | None = Field(None)
    partA: int | None = Field(None)
    partB: int | None = Field(None)
    barcode: str | None = Field(None)
    file: str | None = Field(None, description="Base64-encoded PNG/SVG")


class StickersResponse(BaseModel):
    """Ответ POST /api/v3/orders/stickers."""
    stickers: list[StickerItem] = Field(default=[])


class OrderMetaDetail(BaseModel):
    imei: str | None = None
    uin: str | None = None
    gtin: str | None = None
    sgtin: str | None = None


class OrderMetaItem(BaseModel):
    id: int | None = None
    meta: dict | Any = None
    metaDetails: dict | Any = None


class OrderMetaResponse(BaseModel):
    """Ответ POST /api/marketplace/v3/orders/meta."""
    data: list[OrderMetaItem] | Any = Field(default=None)


# Алиасы для совместимости
Sticker = StickerItem
OrderStatus = OrderStatusInfo


class OrderStatusRequest(BaseModel):
    """POST /api/v3/orders/status — запрос статусов."""
    orders: list[int] = Field(default=[], description="Список ID заказов")


class StickersRequest(BaseModel):
    """POST /api/v3/orders/stickers — запрос стикеров."""
    orders: list[int] = Field(default=[], description="Список ID заказов")


class ClientOrdersRequest(BaseModel):
    """POST /api/v3/orders/client — запрос данных клиента."""
    orders: list[int] = Field(default=[], description="Список ID заказов")


class OrderMetaRequest(BaseModel):
    """POST /api/marketplace/v3/orders/meta — запрос метаданных."""
    orders: list[int] = Field(default=[], description="Список ID заказов")


class SetSgtinRequest(BaseModel):
    sgtin: str = Field(description="Код маркировки КИЗ (честный знак)")


class SetUinRequest(BaseModel):
    uin: str = Field(description="УИН ювелирного изделия")


class SetImeiRequest(BaseModel):
    imei: str = Field(description="IMEI мобильного устройства")


class SetGtinRequest(BaseModel):
    gtin: str = Field(description="GTIN товара")


class SetExpirationRequest(BaseModel):
    expirationDate: str = Field(description="Срок годности (ISO 8601)")


class SetCustomsRequest(BaseModel):
    customsDeclarationNumber: str = Field(description="Номер таможенной декларации (ГТД)")

"""Схемы: FBS — Сборочные задания (заказы)."""
from typing import Any
from pydantic import BaseModel, Field


class Order(BaseModel):
    """Сборочное задание FBS."""
    orderId: int | None = Field(None, description="ID сборочного задания")
    date: str | None = Field(None, description="Дата создания заказа (ISO 8601)")
    lastChangeDate: str | None = Field(None, description="Дата последнего изменения статуса (ISO 8601)")
    warehouseName: str | None = Field(None, description="Склад WB, с которого идёт отгрузка")
    countryName: str | None = Field(None, description="Страна доставки")
    oblastOkrugName: str | None = Field(None, description="Федеральный округ доставки")
    regionName: str | None = Field(None, description="Регион доставки")
    orderUID: str | None = Field(None, description="Уникальный идентификатор заказа (UUID)")
    article: str | None = Field(None, description="Артикул продавца")
    colorCode: str | None = Field(None, description="Код цвета товара")
    rid: str | None = Field(None, description="Уникальный идентификатор позиции заказа")
    totalPrice: float | None = Field(None, description="Цена без скидок, руб.")
    discountPercent: int | None = Field(None, description="Скидка продавца, %")
    spp: int | None = Field(None, description="Скидка по программе WB (СПП), %")
    finishedPrice: float | None = Field(None, description="Итоговая цена с учётом всех скидок, руб.")
    priceWithDisc: float | None = Field(None, description="Цена после скидки продавца, руб.")
    isCancel: bool = Field(default=False, description="Признак отменённого заказа")
    cancelDate: str | None = Field(None, description="Дата отмены заказа (ISO 8601)")
    orderType: str | None = Field(
        None,
        description="Тип заказа: `Клиентский`, `Возврат Брака`, `Принудительный возврат`, `Возврат обезлички`",
    )
    nmId: int | None = Field(None, description="Артикул WB (nmID)")
    chrtId: int | None = Field(None, description="ID характеристики размера (chrtID)")
    price: float | None = Field(None, description="Цена, коп×100 (напр. 300000 = 3000 ₽)")
    convertedPrice: float | None = Field(None, description="Цена в валюте расчётов продавца")
    currencyCode: int | None = Field(None, description="Числовой код валюты (ISO 4217, напр. 643 = RUB)")
    quantity: int | None = Field(None, description="Количество товара в заказе")
    subject: str | None = Field(None, description="Предмет (подкатегория) товара")
    category: str | None = Field(None, description="Родительская категория товара")
    brand: str | None = Field(None, description="Бренд товара")
    name: str | None = Field(None, description="Наименование товара")
    techSize: str | None = Field(None, description="Технический размер (напр. '42', 'XL')")
    skus: list[str] = Field(default=[], description="Баркоды (EAN-13) товара")
    isZeroOrder: bool = Field(default=False, description="Нулевой (тестовый) заказ без реальной оплаты")


class OrdersResponse(BaseModel):
    """Список сборочных заданий."""
    orders: list[Order] = Field(default=[], description="Сборочные задания")


class OrderStatus(BaseModel):
    """Статус сборочного задания."""
    orderId: int = Field(description="ID сборочного задания")
    supplierStatus: str | None = Field(
        None,
        description=(
            "Статус продавца: "
            "`confirm` — подтверждён, "
            "`pack` — собран, "
            "`deliver` — передан в доставку, "
            "`reshipment` — повторная отгрузка, "
            "`cancel` — отменён продавцом."
        ),
    )
    wbStatus: str | None = Field(
        None,
        description=(
            "Статус WB: "
            "`waiting` — ожидает сборки, "
            "`sorted` — отсортирован, "
            "`sold` — выкуплен, "
            "`canceled` — отменён WB."
        ),
    )


class OrderStatusRequest(BaseModel):
    """Запрос статусов сборочных заданий."""
    orders: list[int] = Field(
        description="Список ID сборочных заданий. Максимум **1000** за запрос.",
        max_length=1000,
    )


class OrderStatusResponse(BaseModel):
    """Статусы сборочных заданий."""
    orders: list[OrderStatus] = Field(default=[], description="Статусы запрошенных заданий")


class Sticker(BaseModel):
    """Стикер (этикетка) для сборочного задания."""
    orderId: int | None = Field(None, description="ID сборочного задания")
    partA: int | None = Field(None, description="Первая часть числового кода на стикере")
    partB: int | None = Field(None, description="Вторая часть числового кода на стикере")
    barcode: str | None = Field(None, description="Полный штрихкод стикера")
    file: str | None = Field(None, description="Стикер в формате base64 (SVG или PNG в зависимости от запроса)")


class StickersRequest(BaseModel):
    """Запрос стикеров для сборочных заданий."""
    orders: list[int] = Field(description="Список ID сборочных заданий для получения стикеров")


class StickersResponse(BaseModel):
    """Стикеры сборочных заданий."""
    stickers: list[Sticker] = Field(default=[], description="Стикеры для печати")


class OrderMetaRequest(BaseModel):
    """Запрос метаданных сборочных заданий."""
    orders: list[int] = Field(description="Список ID сборочных заданий")


class OrderMetaResponse(BaseModel):
    """Метаданные сборочных заданий."""
    data: list[Any] | None = Field(None, description="Метаданные (коды маркировки, IMEI и др.)")


class SetSgtinRequest(BaseModel):
    """Код маркировки товара (честный знак)."""
    sgtin: str = Field(description="SGTIN — код маркировки товара (КИЗ/честный знак, 18 или 20 символов)")


class SetUinRequest(BaseModel):
    """УИН ювелирного изделия."""
    uin: str = Field(description="УИН — уникальный идентификационный номер ювелирного изделия")


class SetImeiRequest(BaseModel):
    """IMEI мобильного устройства."""
    imei: str = Field(description="IMEI — международный идентификатор мобильного оборудования (15 цифр)")


class SetGtinRequest(BaseModel):
    """GTIN товара."""
    gtin: str = Field(description="GTIN — глобальный идентификатор торговой единицы (8, 12, 13 или 14 цифр)")


class SetExpirationRequest(BaseModel):
    """Срок годности товара."""
    expirationDate: str = Field(description="Срок годности в формате `YYYY-MM-DD`")


class SetCustomsRequest(BaseModel):
    """Номер таможенной декларации."""
    customsDeclarationNumber: str = Field(
        description="Номер грузовой таможенной декларации (ГТД) для товаров из-за рубежа"
    )


class ClientOrdersRequest(BaseModel):
    """Запрос заказов с данными клиента."""
    orders: list[int] = Field(description="Список ID сборочных заданий для получения данных покупателя")

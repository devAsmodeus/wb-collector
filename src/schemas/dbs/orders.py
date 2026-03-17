"""Схемы: DBS — Сборочные задания (доставка продавца)."""
from pydantic import BaseModel, Field


class DBSOrder(BaseModel):
    """Сборочное задание DBS."""
    orderId: int | None = Field(None, description="ID сборочного задания")
    date: str | None = Field(None, description="Дата создания заказа (ISO 8601)")
    lastChangeDate: str | None = Field(None, description="Дата последнего изменения статуса (ISO 8601)")
    warehouseName: str | None = Field(None, description="Склад / ПВЗ назначения")
    countryName: str | None = Field(None, description="Страна доставки")
    oblastOkrugName: str | None = Field(None, description="Федеральный округ доставки")
    regionName: str | None = Field(None, description="Регион доставки")
    orderUID: str | None = Field(None, description="Уникальный идентификатор заказа (UUID)")
    article: str | None = Field(None, description="Артикул продавца")
    rid: str | None = Field(None, description="Уникальный идентификатор позиции заказа")
    totalPrice: float | None = Field(None, description="Цена без скидок, руб.")
    discountPercent: int | None = Field(None, description="Скидка продавца, %")
    spp: int | None = Field(None, description="Скидка СПП, %")
    finishedPrice: float | None = Field(None, description="Итоговая цена с учётом всех скидок, руб.")
    priceWithDisc: float | None = Field(None, description="Цена после скидки продавца, руб.")
    isCancel: bool = Field(default=False, description="Признак отменённого заказа")
    cancelDate: str | None = Field(None, description="Дата отмены (ISO 8601)")
    orderType: str | None = Field(None, description="Тип заказа")
    nmId: int | None = Field(None, description="Артикул WB (nmID)")
    chrtId: int | None = Field(None, description="ID характеристики размера")
    price: float | None = Field(None, description="Цена, коп×100")
    convertedPrice: float | None = Field(None, description="Цена в валюте расчётов")
    currencyCode: int | None = Field(None, description="Числовой код валюты (ISO 4217)")
    quantity: int | None = Field(None, description="Количество товара")
    subject: str | None = Field(None, description="Предмет товара")
    category: str | None = Field(None, description="Категория товара")
    brand: str | None = Field(None, description="Бренд")
    name: str | None = Field(None, description="Наименование товара")
    techSize: str | None = Field(None, description="Технический размер")
    skus: list[str] = Field(default=[], description="Баркоды (EAN-13) товара")
    requiredMeta: list[str] = Field(
        default=[],
        description="Обязательные метаданные (напр. `imei`). Без заполнения нельзя перевести в доставку.",
    )


class DBSOrdersResponse(BaseModel):
    """Список сборочных заданий DBS."""
    orders: list[DBSOrder] = Field(default=[], description="Сборочные задания DBS")


class DBSOrderIdsRequest(BaseModel):
    """Запрос по списку ID заданий DBS."""
    orders: list[int] = Field(description="Список ID сборочных заданий")


class DBSOrderStatusItem(BaseModel):
    """Статус сборочного задания DBS."""
    orderId: int = Field(description="ID сборочного задания")
    supplierStatus: str | None = Field(
        None,
        description=(
            "Статус продавца: `confirm` — подтверждён, `assemble` — собирается, "
            "`deliver` — в доставке, `receive` — получен покупателем, "
            "`reject` — отказ, `cancel` — отменён."
        ),
    )
    wbStatus: str | None = Field(
        None,
        description="Статус WB: `waiting`, `sorted`, `sold`, `canceled`.",
    )


class DBSOrderStatusResponse(BaseModel):
    """Статусы сборочных заданий DBS."""
    orders: list[DBSOrderStatusItem] = Field(default=[], description="Статусы заданий")


class DBSDeliveryDateRequest(BaseModel):
    """Установка даты и времени доставки."""
    orders: list[int] = Field(description="Список ID сборочных заданий")
    deliveryDate: str = Field(description="Дата и время доставки покупателю (ISO 8601, напр. `2024-03-15T14:00:00`)")


class DBSRejectRequest(BaseModel):
    """Отказ от заказов или отказ покупателя."""
    orders: list[int] = Field(description="Список ID сборочных заданий")
    reason: str | None = Field(None, description="Причина отказа")


class DBSReceiveRequest(BaseModel):
    """Уведомление о получении заказа покупателем."""
    orders: list[int] = Field(description="Список ID сборочных заданий, полученных покупателем")


class DBSSticker(BaseModel):
    """Стикер для задания DBS."""
    orderId: int | None = Field(None, description="ID сборочного задания")
    partA: int | None = Field(None, description="Первая часть кода стикера")
    partB: int | None = Field(None, description="Вторая часть кода стикера")
    barcode: str | None = Field(None, description="Штрихкод стикера")
    file: str | None = Field(None, description="Стикер в формате base64")


class DBSStickersResponse(BaseModel):
    """Стикеры заданий DBS."""
    stickers: list[DBSSticker] = Field(default=[], description="Стикеры для печати")


class DBSGroupInfoRequest(BaseModel):
    """Запрос информации о платной доставке."""
    orders: list[int] = Field(description="Список ID сборочных заданий для получения информации о тарифе доставки")

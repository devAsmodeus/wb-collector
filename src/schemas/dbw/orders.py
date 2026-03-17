"""Схемы: DBW — Сборочные задания (доставка WB)."""
from pydantic import BaseModel, Field


class DBWOrder(BaseModel):
    """Сборочное задание DBW."""
    orderId: int | None = Field(None, description="ID сборочного задания")
    date: str | None = Field(None, description="Дата создания заказа (ISO 8601)")
    lastChangeDate: str | None = Field(None, description="Дата последнего изменения статуса (ISO 8601)")
    warehouseName: str | None = Field(None, description="Склад WB, с которого идёт отгрузка")
    countryName: str | None = Field(None, description="Страна доставки")
    oblastOkrugName: str | None = Field(None, description="Федеральный округ доставки")
    regionName: str | None = Field(None, description="Регион доставки")
    orderUID: str | None = Field(None, description="Уникальный идентификатор заказа (UUID)")
    article: str | None = Field(None, description="Артикул продавца")
    rid: str | None = Field(None, description="Уникальный идентификатор позиции заказа")
    totalPrice: float | None = Field(None, description="Цена без скидок, руб.")
    discountPercent: int | None = Field(None, description="Скидка продавца, %")
    spp: int | None = Field(None, description="Скидка по программе WB (СПП), %")
    finishedPrice: float | None = Field(None, description="Итоговая цена с учётом всех скидок, руб.")
    priceWithDisc: float | None = Field(None, description="Цена после скидки продавца, руб.")
    isCancel: bool = Field(default=False, description="Признак отменённого заказа")
    cancelDate: str | None = Field(None, description="Дата отмены заказа (ISO 8601)")
    orderType: str | None = Field(None, description="Тип заказа")
    nmId: int | None = Field(None, description="Артикул WB (nmID)")
    chrtId: int | None = Field(None, description="ID характеристики размера (chrtID)")
    price: float | None = Field(None, description="Цена, коп×100")
    convertedPrice: float | None = Field(None, description="Цена в валюте расчётов продавца")
    currencyCode: int | None = Field(None, description="Числовой код валюты (ISO 4217)")
    quantity: int | None = Field(None, description="Количество товара в заказе")
    subject: str | None = Field(None, description="Предмет (подкатегория) товара")
    category: str | None = Field(None, description="Родительская категория товара")
    brand: str | None = Field(None, description="Бренд товара")
    name: str | None = Field(None, description="Наименование товара")
    techSize: str | None = Field(None, description="Технический размер")
    skus: list[str] = Field(default=[], description="Баркоды (EAN-13) товара")
    requiredMeta: list[str] = Field(
        default=[],
        description="Обязательные метаданные для этого задания (напр. `imei`, `sgtin`). "
                    "Без их заполнения задание нельзя передать в доставку.",
    )


class DBWOrdersResponse(BaseModel):
    """Список сборочных заданий DBW."""
    orders: list[DBWOrder] = Field(default=[], description="Сборочные задания DBW")


class DBWOrderStatusItem(BaseModel):
    """Статус одного сборочного задания DBW."""
    orderId: int = Field(description="ID сборочного задания")
    supplierStatus: str | None = Field(
        None,
        description=(
            "Статус продавца: "
            "`confirm` — подтверждён, "
            "`assemble` — собирается, "
            "`assembled` — собран, "
            "`deliver` — передан в доставку, "
            "`cancel` — отменён."
        ),
    )
    wbStatus: str | None = Field(
        None,
        description=(
            "Статус WB: "
            "`waiting` — ожидает подтверждения, "
            "`sorted` — отсортирован, "
            "`sold` — выкуплен, "
            "`canceled` — отменён WB."
        ),
    )


class DBWOrderStatusRequest(BaseModel):
    """Запрос статусов сборочных заданий DBW."""
    orders: list[int] = Field(description="Список ID сборочных заданий DBW.")


class DBWOrderStatusResponse(BaseModel):
    """Статусы сборочных заданий DBW."""
    orders: list[DBWOrderStatusItem] = Field(default=[], description="Статусы запрошенных заданий")


class DBWDeliveryDateRequest(BaseModel):
    """Установка даты доставки для сборочного задания DBW."""
    orders: list[int] = Field(description="Список ID сборочных заданий, для которых устанавливается дата доставки")
    deliveryDate: str = Field(
        description="Планируемая дата доставки покупателю в формате `YYYY-MM-DD`"
    )


class DBWClientOrdersRequest(BaseModel):
    """Запрос заказов DBW с данными клиента."""
    orders: list[int] = Field(description="Список ID сборочных заданий для получения данных покупателя")


class DBWSticker(BaseModel):
    """Стикер для сборочного задания DBW."""
    orderId: int | None = Field(None, description="ID сборочного задания")
    partA: int | None = Field(None, description="Первая часть числового кода на стикере")
    partB: int | None = Field(None, description="Вторая часть числового кода на стикере")
    barcode: str | None = Field(None, description="Полный штрихкод стикера")
    file: str | None = Field(None, description="Стикер в формате base64")


class DBWStickersRequest(BaseModel):
    """Запрос стикеров для сборочных заданий DBW."""
    orders: list[int] = Field(description="Список ID сборочных заданий для получения стикеров")


class DBWStickersResponse(BaseModel):
    """Стикеры сборочных заданий DBW."""
    stickers: list[DBWSticker] = Field(default=[], description="Стикеры для печати")


class DBWCourierRequest(BaseModel):
    """Вызов курьера для сборочного задания DBW."""
    orders: list[int] = Field(description="Список ID сборочных заданий для передачи курьеру WB")

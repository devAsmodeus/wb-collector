"""Схемы: Самовывоз (Click & Collect) — Сборочные задания."""
from pydantic import BaseModel, Field


class PickupOrder(BaseModel):
    """Сборочное задание Самовывоз."""
    orderId: int | None = Field(None, description="ID сборочного задания")
    date: str | None = Field(None, description="Дата создания заказа (ISO 8601)")
    lastChangeDate: str | None = Field(None, description="Дата последнего изменения статуса (ISO 8601)")
    warehouseName: str | None = Field(None, description="ПВЗ / пункт самовывоза")
    countryName: str | None = Field(None, description="Страна")
    oblastOkrugName: str | None = Field(None, description="Федеральный округ")
    regionName: str | None = Field(None, description="Регион")
    orderUID: str | None = Field(None, description="Уникальный идентификатор заказа (UUID)")
    article: str | None = Field(None, description="Артикул продавца")
    rid: str | None = Field(None, description="Уникальный идентификатор позиции заказа")
    totalPrice: float | None = Field(None, description="Цена без скидок, руб.")
    discountPercent: int | None = Field(None, description="Скидка продавца, %")
    spp: int | None = Field(None, description="Скидка СПП, %")
    finishedPrice: float | None = Field(None, description="Итоговая цена, руб.")
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
        description="Обязательные метаданные для заполнения перед выдачей товара покупателю.",
    )


class PickupOrdersResponse(BaseModel):
    """Список сборочных заданий Самовывоз."""
    orders: list[PickupOrder] = Field(default=[], description="Сборочные задания Самовывоз")


class PickupOrderIdsRequest(BaseModel):
    """Запрос по списку ID заданий."""
    orders: list[int] = Field(description="Список ID сборочных заданий")


class PickupOrderStatusItem(BaseModel):
    """Статус сборочного задания Самовывоз."""
    orderId: int = Field(description="ID сборочного задания")
    supplierStatus: str | None = Field(
        None,
        description=(
            "Статус продавца: `confirm` — подтверждён, `prepare` — подготовлен, "
            "`receive` — выдан покупателю, `reject` — отказ, `cancel` — отменён."
        ),
    )
    wbStatus: str | None = Field(None, description="Статус WB: `waiting`, `sorted`, `sold`, `canceled`.")


class PickupOrderStatusResponse(BaseModel):
    """Статусы сборочных заданий Самовывоз."""
    orders: list[PickupOrderStatusItem] = Field(default=[], description="Статусы заданий")


class PickupRejectRequest(BaseModel):
    """Отказ от заданий."""
    orders: list[int] = Field(description="Список ID сборочных заданий")
    reason: str | None = Field(None, description="Причина отказа")


class PickupReceiveRequest(BaseModel):
    """Уведомление о выдаче товара покупателю."""
    orders: list[int] = Field(description="Список ID сборочных заданий, выданных покупателю")

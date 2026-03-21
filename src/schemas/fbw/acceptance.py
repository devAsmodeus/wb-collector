"""Схемы: FBW — Информация для формирования поставок."""
from pydantic import BaseModel, Field


class FBWGoodItem(BaseModel):
    """Товар для расчёта опций приёмки."""
    quantity: int = Field(
        description="Суммарное количество товаров, планируемых для поставки. Максимум 5000 позиций в запросе.",
        ge=1,
    )
    barcode: str = Field(description="Баркод из карточки товара (EAN-13)")


class FBWAcceptanceOptionsRequest(BaseModel):
    """Запрос опций приёмки FBW.

    Массив товаров передаётся в теле запроса.
    Склад назначения опционально фильтруется через query-параметр `warehouseID`.
    """
    goods: list[FBWGoodItem] = Field(
        description="Список товаров для расчёта опций приёмки. Максимум 5000 позиций.",
        max_length=5000,
    )


class FBWAcceptanceWarehouse(BaseModel):
    """Склад в ответе опций приёмки."""
    warehouseID: int | None = Field(None, description="ID склада WB")
    canBox: bool | None = Field(None, description="Доступен тип упаковки Короб")
    canMonopallet: bool | None = Field(None, description="Доступен тип упаковки Монопаллета")
    canSupersafe: bool | None = Field(None, description="Доступен тип упаковки Суперсейф")
    isBoxOnPallet: bool | None = Field(None, description="Доступен тип поставки Поштучная паллета")


class FBWAcceptanceError(BaseModel):
    """Ошибка в ответе опций приёмки."""
    title: str | None = Field(None, description="ID ошибки")
    detail: str | None = Field(None, description="Описание ошибки")


class FBWAcceptanceResultItem(BaseModel):
    """Элемент ответа опций приёмки (по баркоду)."""
    barcode: str | None = Field(None, description="Баркод товара из карточки")
    isError: bool | None = Field(None, description="Наличие ошибки: `true` — есть, поля нет — нет")
    error: FBWAcceptanceError | None = Field(None, description="Данные ошибки (при наличии)")
    warehouses: list[FBWAcceptanceWarehouse] | None = Field(None, description="Список складов с опциями приёмки. `null` при ошибке")


class FBWAcceptanceOptionsResponse(BaseModel):
    """Ответ метода опций приёмки FBW."""
    result: list[FBWAcceptanceResultItem] = Field(default=[], description="Результаты по каждому баркоду")
    requestId: str | None = Field(None, description="ID запроса при наличии ошибок")


class FBWWarehouse(BaseModel):
    """Склад WB для FBW-поставок."""
    id: int | None = Field(None, description="ID склада WB")
    name: str | None = Field(None, description="Название склада")
    address: str | None = Field(None, description="Адрес склада")
    workTime: str | None = Field(None, description="Режим работы склада")
    acceptsQR: bool | None = Field(None, description="Принимает ли склад поставки по QR-коду")


class FBWWarehousesResponse(BaseModel):
    """Список складов WB для FBW."""
    warehouses: list[FBWWarehouse] = Field(default=[], description="Склады WB, принимающие FBW-поставки")


class FBWBoxTariff(BaseModel):
    """Тариф за транзит коробов."""
    warehouseName: str | None = Field(None, description="Название промежуточного склада")
    tariff: int | None = Field(None, description="Тариф за коробку, руб.")


class FBWTransitTariff(BaseModel):
    """Тариф транзитной доставки FBW."""
    transitWarehouseName: str | None = Field(None, description="Транзитный склад")
    destinationWarehouseName: str | None = Field(None, description="Склад назначения")
    activeFrom: str | None = Field(None, description="С какого числа доступно транзитное направление (ISO 8601)")
    boxTariff: list[FBWBoxTariff] | None = Field(
        None,
        description="Тариф за транзит коробов. `null` — транзит для коробов недоступен.",
    )
    palletTariff: int | None = Field(None, description="Тариф за паллету, руб.")


class FBWTransitTariffsResponse(BaseModel):
    """Тарифы транзитной доставки FBW."""
    tariffs: list[FBWTransitTariff] = Field(default=[], description="Тарифы по направлениям транзита")

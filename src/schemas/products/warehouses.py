"""Схемы: Товары — Склады и остатки."""
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Остатки
# ---------------------------------------------------------------------------

class StockItem(BaseModel):
    """Остаток товара на складе продавца."""
    sku: str = Field(description="Баркод (EAN-13) товара")
    amount: int = Field(description="Количество единиц на складе")


class StocksRequest(BaseModel):
    """Тело запроса для получения остатков на складе."""
    skus: list[str] = Field(
        description=(
            "Список баркодов (EAN-13) товаров, по которым нужны остатки.\n"
            "Максимум **1000 баркодов** за один запрос."
        ),
        min_length=1,
        max_length=1000,
    )


class StocksResponse(BaseModel):
    """Ответ с остатками товаров на складе."""
    stocks: list[StockItem] = Field(default=[], description="Список остатков по баркодам")


# ---------------------------------------------------------------------------
# Склады WB (офисы)
# ---------------------------------------------------------------------------

class WBOffice(BaseModel):
    """Склад (офис) WB — точка приёмки товара от продавца."""
    id: int | None = Field(None, description="ID офиса WB")
    name: str | None = Field(None, description="Название склада WB (напр. 'Коледино', 'Электросталь')")
    address: str | None = Field(None, description="Полный адрес склада")
    city: str | None = Field(None, description="Город расположения склада")
    longitude: float | None = Field(None, description="Долгота (координаты склада)")
    latitude: float | None = Field(None, description="Широта (координаты склада)")
    selected: bool = Field(default=False, description="Выбран ли склад по умолчанию для отгрузки")

    model_config = {"extra": "allow"}


class WBOfficesResponse(BaseModel):
    """Ответ со списком складов WB."""
    result: list[WBOffice] | None = Field(None, description="Список складов WB (офисов приёмки)")


# ---------------------------------------------------------------------------
# Склады продавца
# ---------------------------------------------------------------------------

class SellerWarehouse(BaseModel):
    """Склад продавца (для схемы FBS — отгрузка со своего склада)."""
    id: int | None = Field(None, description="Внутренний ID склада продавца")
    warehouseId: int | None = Field(None, description="ID склада в системе WB")
    name: str | None = Field(None, description="Название склада продавца")
    officeId: int | None = Field(
        None,
        description="ID офиса WB, к которому привязан склад продавца",
    )
    isProcessing: bool | None = Field(
        None,
        description="Обрабатывает ли склад заказы в данный момент",
    )
    cargoType: int | None = Field(
        None,
        description=(
            "Тип доставки: "
            "`1` — короба, "
            "`2` — монопаллеты, "
            "`3` — суперсейф."
        ),
    )

    model_config = {"extra": "allow"}


class SellerWarehousesResponse(BaseModel):
    """Ответ со списком складов продавца."""
    result: list[SellerWarehouse] | None = Field(
        None,
        description="Список складов продавца",
    )

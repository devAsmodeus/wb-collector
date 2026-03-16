"""Схемы: Работа с товарами — Остатки и склады продавца."""
from pydantic import BaseModel


class StockItem(BaseModel):
    sku: str
    amount: int


class WBOffice(BaseModel):
    id: int | None = None
    name: str | None = None
    address: str | None = None
    city: str | None = None
    longitude: float | None = None
    latitude: float | None = None
    selected: bool = False

    class Config:
        extra = "allow"


class WBOfficesResponse(BaseModel):
    result: list[WBOffice] | None = None


class SellerWarehouse(BaseModel):
    id: int | None = None
    warehouseId: int | None = None
    name: str | None = None
    officeId: int | None = None
    isProcessing: bool | None = None
    cargoType: int | None = None

    class Config:
        extra = "allow"


class SellerWarehousesResponse(BaseModel):
    result: list[SellerWarehouse] | None = None


class DBWContact(BaseModel):
    name: str | None = None
    phone: str | None = None
    email: str | None = None


class DBWContactsResponse(BaseModel):
    result: list[DBWContact] | None = None

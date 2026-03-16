"""Схемы: Работа с товарами — Цены и скидки."""
from typing import Any
from pydantic import BaseModel


class GoodsSize(BaseModel):
    # WB реально возвращает sizeID (расхождение с документацией)
    chrtID: int | None = None
    sizeID: int | None = None
    techSize: str | None = None
    techSizeName: str | None = None
    skus: list[str] = []
    price: int | None = None
    discountedPrice: int | None = None
    clubDiscountedPrice: int | None = None

    @property
    def size_id(self) -> int | None:
        return self.chrtID or self.sizeID


class GoodsItem(BaseModel):
    nmID: int
    vendorCode: str = ""
    sizes: list[GoodsSize] = []
    currencyIsoCode4217: str = "RUB"
    discount: int = 0
    clubDiscount: int = 0
    editableSizePrice: bool = False


class GoodsListData(BaseModel):
    listGoods: list[GoodsItem] = []


class GoodsListResponse(BaseModel):
    data: GoodsListData | None = None
    error: bool = False
    errorText: str = ""


class PriceTaskRequest(BaseModel):
    nmID: int
    price: int | None = None
    discount: int | None = None


class PriceHistoryTask(BaseModel):
    uploadID: int | None = None
    status: str | None = None
    uploadDate: str | None = None
    activationDate: str | None = None


class PriceHistoryResponse(BaseModel):
    data: list[PriceHistoryTask] | Any = None
    error: bool = False
    errorText: str = ""

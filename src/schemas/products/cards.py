"""Схемы: Работа с товарами — Карточки товаров."""
from typing import Any
from pydantic import BaseModel


class CardPhoto(BaseModel):
    big: str | None = None
    c246x328: str | None = None
    c516x688: str | None = None
    square: str | None = None
    tm: str | None = None


class CardSize(BaseModel):
    chrtID: int | None = None
    techSize: str = ""
    wbSize: str = ""
    skus: list[str] = []
    price: int | None = None


class CardCharacteristic(BaseModel):
    id: int
    name: str
    value: Any = None


class CardTag(BaseModel):
    id: int
    name: str
    color: str


class CardDimensions(BaseModel):
    length: float | None = None
    width: float | None = None
    height: float | None = None
    weightBrutto: float | None = None


class ProductCard(BaseModel):
    nmID: int
    imtID: int | None = None
    nmUUID: str | None = None
    subjectID: int | None = None
    subjectName: str | None = None
    vendorCode: str = ""
    brand: str = ""
    title: str = ""
    description: str = ""
    needKiz: bool = False
    photos: list[CardPhoto] = []
    video: str | None = None
    dimensions: CardDimensions | None = None
    characteristics: list[CardCharacteristic] = []
    sizes: list[CardSize] = []
    tags: list[CardTag] = []
    createdAt: str | None = None
    updatedAt: str | None = None


class CardCursor(BaseModel):
    updatedAt: str | None = None
    nmID: int | None = None
    total: int = 0


class CardsListResponse(BaseModel):
    cards: list[ProductCard] = []
    cursor: CardCursor | None = None


class CardsListSettings(BaseModel):
    cursor: dict | None = None
    filter: dict | None = None
    sort: dict | None = None


class CardsListRequest(BaseModel):
    settings: CardsListSettings | None = None


class CardLimits(BaseModel):
    freeToUse: int | None = None
    freeLimitBase: int | None = None
    paidLimitBase: int | None = None
    used: int | None = None


class CardLimitsResponse(BaseModel):
    error: bool = False
    errorText: str = ""
    data: CardLimits | Any = None


class BarcodesResponse(BaseModel):
    error: bool = False
    errorText: str = ""
    data: list[str] = []


class CardErrorItem(BaseModel):
    batchUUID: str | None = None
    vendorCodes: list[str] = []
    errors: dict | None = None
    subjects: dict | None = None
    brands: dict | None = None


class CardErrorCursor(BaseModel):
    next: bool = False
    updatedAt: str | None = None
    batchUUID: str | None = None


class CardErrorData(BaseModel):
    items: list[CardErrorItem] = []
    cursor: CardErrorCursor | None = None


class CardErrorsResponse(BaseModel):
    error: bool = False
    errorText: str = ""
    data: CardErrorData | None = None

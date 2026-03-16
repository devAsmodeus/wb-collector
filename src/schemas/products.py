"""Pydantic схемы для 02-products WB API."""
from typing import Any
from pydantic import BaseModel


# ─── Общий враппер ответа WB ─────────────────────────────────────────────────

class WBResponse(BaseModel):
    error: bool = False
    errorText: str = ""
    additionalErrors: Any = None


# ─── Справочники ─────────────────────────────────────────────────────────────

class ParentCategory(BaseModel):
    id: int | None = None
    name: str | None = None


class ParentCategoriesResponse(WBResponse):
    data: list[ParentCategory] | Any = None


class Subject(BaseModel):
    subjectID: int
    parentID: int
    subjectName: str
    parentName: str


class SubjectsResponse(WBResponse):
    data: list[Subject] = []


class SubjectCharc(BaseModel):
    charcID: int
    subjectName: str
    subjectID: int
    name: str
    required: bool = False
    unitName: str = ""
    maxCount: int = 0
    popular: bool = False
    charcType: int = 1


class SubjectCharcsResponse(WBResponse):
    data: list[SubjectCharc] = []


class TnvedCode(BaseModel):
    tnved: str
    isKiz: bool = False


class TnvedResponse(WBResponse):
    data: list[TnvedCode] = []


class Brand(BaseModel):
    id: int
    name: str
    logoUrl: str | None = None


class BrandsResponse(BaseModel):
    brands: list[Brand] = []
    next: int | None = None
    total: int = 0


# ─── Ярлыки ──────────────────────────────────────────────────────────────────

class Tag(BaseModel):
    id: int
    name: str
    color: str


class TagCreate(BaseModel):
    name: str
    color: str


class TagUpdate(BaseModel):
    name: str | None = None
    color: str | None = None


class TagsResponse(WBResponse):
    data: list[Tag] | Any = None


# ─── Карточки товаров ────────────────────────────────────────────────────────

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


class CardLimitsResponse(WBResponse):
    data: CardLimits | Any = None


class BarcodesResponse(WBResponse):
    data: list[str] = []


# ─── Ошибки карточек ─────────────────────────────────────────────────────────

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


class CardErrorsResponse(WBResponse):
    data: CardErrorData | None = None


# ─── Цены и скидки ───────────────────────────────────────────────────────────

class GoodsSize(BaseModel):
    # WB API реально возвращает sizeID, не chrtID (расхождение с документацией)
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


# ─── Остатки и склады ────────────────────────────────────────────────────────

class StockItem(BaseModel):
    sku: str
    amount: int


class WarehouseStock(BaseModel):
    warehouseId: int | None = None
    stocks: list[StockItem] = []


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
    # Дополнительные поля из реального ответа WB
    officeId: int | None = None
    isProcessing: bool | None = None
    cargoType: int | None = None
    class Config:
        extra = "allow"


class SellerWarehousesResponse(BaseModel):
    result: list[SellerWarehouse] | None = None


class SellerWarehouseCreate(BaseModel):
    name: str
    officeId: int


class SellerWarehouseUpdate(BaseModel):
    name: str
    officeId: int


class DBWContact(BaseModel):
    name: str | None = None
    phone: str | None = None
    email: str | None = None


class DBWContactsResponse(BaseModel):
    result: list[DBWContact] | None = None

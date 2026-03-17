"""Схемы: Товары — реэкспорт всех подмодулей."""
from src.schemas.products.directories import (
    WBResponse,
    ParentCategory, ParentCategoriesResponse,
    Subject, SubjectsResponse,
    SubjectCharc, SubjectCharcsResponse,
    TnvedCode, TnvedResponse,
    Brand, BrandsResponse,
    DirectoryItem, DirectoryResponse,
)
from src.schemas.products.tags import (
    WBTag, TagsResponse,
    TagCreateRequest, TagUpdateRequest, TagLinkRequest,
)
from src.schemas.products.cards import (
    CardPhoto, CardSize, CardCharacteristic, CardTag, CardDimensions,
    ProductCard, CardCursor, CardsListResponse,
    CardsListRequest, CardLimits, CardLimitsResponse, BarcodesResponse,
    CardErrorItem, CardErrorCursor, CardErrorData, CardErrorsResponse,
)
from src.schemas.products.media import MediaUploadByUrlRequest, MediaUploadResponse
from src.schemas.products.prices import (
    GoodsSize, GoodsItem, GoodsListData, GoodsListResponse,
    PriceHistoryTask, PriceHistoryResponse,
    QuarantineItem, QuarantineData, QuarantineResponse,
    UploadGoodsItem, UploadGoodsData, UploadGoodsResponse,
)
from src.schemas.products.warehouses import (
    StockItem, StocksRequest, StocksResponse,
    WBOffice, WBOfficesResponse,
    SellerWarehouse, SellerWarehousesResponse,
    DBWContact, DBWContactsResponse,
)

__all__ = [
    "WBResponse",
    "ParentCategory", "ParentCategoriesResponse",
    "Subject", "SubjectsResponse",
    "SubjectCharc", "SubjectCharcsResponse",
    "TnvedCode", "TnvedResponse",
    "Brand", "BrandsResponse",
    "DirectoryItem", "DirectoryResponse",
    "WBTag", "TagsResponse",
    "TagCreateRequest", "TagUpdateRequest", "TagLinkRequest",
    "CardPhoto", "CardSize", "CardCharacteristic", "CardTag", "CardDimensions",
    "ProductCard", "CardCursor", "CardsListResponse",
    "CardsListRequest", "CardLimits", "CardLimitsResponse", "BarcodesResponse",
    "CardErrorItem", "CardErrorCursor", "CardErrorData", "CardErrorsResponse",
    "MediaUploadByUrlRequest", "MediaUploadResponse",
    "GoodsSize", "GoodsItem", "GoodsListData", "GoodsListResponse",
    "PriceHistoryTask", "PriceHistoryResponse",
    "QuarantineItem", "QuarantineData", "QuarantineResponse",
    "UploadGoodsItem", "UploadGoodsData", "UploadGoodsResponse",
    "StockItem", "StocksRequest", "StocksResponse",
    "WBOffice", "WBOfficesResponse",
    "SellerWarehouse", "SellerWarehousesResponse",
]

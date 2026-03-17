"""Схемы: FBS — Заказы FBS (пропуска, сборочные задания, поставки)."""
from src.schemas.fbs.passes import (
    PassOffice, PassOfficesResponse,
    Pass, PassesResponse,
    CreatePassRequest, UpdatePassRequest,
)
from src.schemas.fbs.orders import (
    Order, OrdersResponse,
    OrderStatus, OrderStatusRequest, OrderStatusResponse,
    Sticker, StickersRequest, StickersResponse,
    OrderMetaRequest, OrderMetaResponse,
    SetSgtinRequest, SetUinRequest, SetImeiRequest,
    SetGtinRequest, SetExpirationRequest, SetCustomsRequest,
    ClientOrdersRequest,
)
from src.schemas.fbs.supplies import (
    Supply, SuppliesResponse,
    CreateSupplyRequest, CreateSupplyResponse,
    SupplyOrder, SupplyOrdersResponse, SupplyOrderIdsResponse,
    AddOrdersToSupplyRequest, SupplyBarcode,
    Box, BoxesResponse,
    AddBoxesRequest, DeleteBoxesRequest,
    BoxStickersRequest, BoxSticker, BoxStickersResponse,
)

__all__ = [
    "PassOffice", "PassOfficesResponse",
    "Pass", "PassesResponse",
    "CreatePassRequest", "UpdatePassRequest",
    "Order", "OrdersResponse",
    "OrderStatus", "OrderStatusRequest", "OrderStatusResponse",
    "Sticker", "StickersRequest", "StickersResponse",
    "OrderMetaRequest", "OrderMetaResponse",
    "SetSgtinRequest", "SetUinRequest", "SetImeiRequest",
    "SetGtinRequest", "SetExpirationRequest", "SetCustomsRequest",
    "ClientOrdersRequest",
    "Supply", "SuppliesResponse",
    "CreateSupplyRequest", "CreateSupplyResponse",
    "SupplyOrder", "SupplyOrdersResponse", "SupplyOrderIdsResponse",
    "AddOrdersToSupplyRequest", "SupplyBarcode",
    "Box", "BoxesResponse",
    "AddBoxesRequest", "DeleteBoxesRequest",
    "BoxStickersRequest", "BoxSticker", "BoxStickersResponse",
]

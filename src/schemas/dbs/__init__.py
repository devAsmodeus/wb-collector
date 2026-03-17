"""Схемы: DBS — Заказы DBS."""
from src.schemas.dbs.orders import (
    DBSOrder, DBSOrdersResponse,
    DBSOrderIdsRequest, DBSOrderStatusItem,
    DBSOrderStatusResponse, DBSDeliveryDateRequest,
    DBSRejectRequest, DBSReceiveRequest,
    DBSSticker, DBSStickersResponse, DBSGroupInfoRequest,
)
from src.schemas.dbs.meta import (
    DBSMetaInfoRequest, DBSMetaDeleteRequest,
    DBSSgtinItem, DBSSetSgtinRequest,
    DBSUinItem, DBSSetUinRequest,
    DBSImeiItem, DBSSetImeiRequest,
    DBSGtinItem, DBSSetGtinRequest,
    DBSCustomsItem, DBSSetCustomsRequest,
    DBSSetSgtinSingleRequest, DBSSetUinSingleRequest,
    DBSSetImeiSingleRequest, DBSSetGtinSingleRequest,
)

__all__ = [
    "DBSOrder", "DBSOrdersResponse",
    "DBSOrderIdsRequest", "DBSOrderStatusItem",
    "DBSOrderStatusResponse", "DBSDeliveryDateRequest",
    "DBSRejectRequest", "DBSReceiveRequest",
    "DBSSticker", "DBSStickersResponse", "DBSGroupInfoRequest",
    "DBSMetaInfoRequest", "DBSMetaDeleteRequest",
    "DBSSgtinItem", "DBSSetSgtinRequest",
    "DBSUinItem", "DBSSetUinRequest",
    "DBSImeiItem", "DBSSetImeiRequest",
    "DBSGtinItem", "DBSSetGtinRequest",
    "DBSCustomsItem", "DBSSetCustomsRequest",
    "DBSSetSgtinSingleRequest", "DBSSetUinSingleRequest",
    "DBSSetImeiSingleRequest", "DBSSetGtinSingleRequest",
]

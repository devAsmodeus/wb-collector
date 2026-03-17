"""Сервис: Самовывоз — Метаданные."""
from src.collectors.pickup.meta import PickupMetaCollector
from src.schemas.pickup.meta import (
    PickupMetaInfoRequest, PickupMetaDeleteRequest,
    PickupSetSgtinRequest, PickupSetUinRequest,
    PickupSetImeiRequest, PickupSetGtinRequest,
    PickupSetSgtinSingleRequest, PickupSetUinSingleRequest,
    PickupSetImeiSingleRequest, PickupSetGtinSingleRequest,
)
from src.services.base import BaseService


class PickupMetaService(BaseService):

    async def get_meta_info(self, data: PickupMetaInfoRequest) -> dict:
        async with PickupMetaCollector() as c:
            return await c.get_meta_info(data.orders)

    async def delete_meta(self, data: PickupMetaDeleteRequest) -> None:
        async with PickupMetaCollector() as c:
            await c.delete_meta(data.orders, data.key)

    async def set_sgtin(self, data: PickupSetSgtinRequest) -> dict:
        async with PickupMetaCollector() as c:
            return await c.set_sgtin([o.model_dump() for o in data.orders])

    async def set_uin(self, data: PickupSetUinRequest) -> dict:
        async with PickupMetaCollector() as c:
            return await c.set_uin([o.model_dump() for o in data.orders])

    async def set_imei(self, data: PickupSetImeiRequest) -> dict:
        async with PickupMetaCollector() as c:
            return await c.set_imei([o.model_dump() for o in data.orders])

    async def set_gtin(self, data: PickupSetGtinRequest) -> dict:
        async with PickupMetaCollector() as c:
            return await c.set_gtin([o.model_dump() for o in data.orders])

    # --- Deprecated ---
    async def get_order_meta(self, order_id: int) -> dict:
        async with PickupMetaCollector() as c:
            return await c.get_order_meta(order_id)

    async def delete_order_meta(self, order_id: int, key: str) -> None:
        async with PickupMetaCollector() as c:
            await c.delete_order_meta(order_id, key)

    async def set_sgtin_single(self, order_id: int, data: PickupSetSgtinSingleRequest) -> dict:
        async with PickupMetaCollector() as c:
            return await c.set_sgtin_single(order_id, data.sgtins)

    async def set_uin_single(self, order_id: int, data: PickupSetUinSingleRequest) -> dict:
        async with PickupMetaCollector() as c:
            return await c.set_uin_single(order_id, data.uin)

    async def set_imei_single(self, order_id: int, data: PickupSetImeiSingleRequest) -> dict:
        async with PickupMetaCollector() as c:
            return await c.set_imei_single(order_id, data.imei)

    async def set_gtin_single(self, order_id: int, data: PickupSetGtinSingleRequest) -> dict:
        async with PickupMetaCollector() as c:
            return await c.set_gtin_single(order_id, data.gtin)

"""Сервис: DBS — Метаданные сборочных заданий."""
from src.collectors.dbs.meta import DBSMetaCollector
from src.schemas.dbs.meta import (
    DBSMetaInfoRequest, DBSMetaDeleteRequest,
    DBSSetSgtinRequest, DBSSetUinRequest, DBSSetImeiRequest,
    DBSSetGtinRequest, DBSSetCustomsRequest,
    DBSSetSgtinSingleRequest, DBSSetUinSingleRequest,
    DBSSetImeiSingleRequest, DBSSetGtinSingleRequest,
)
from src.services.base import BaseService


class DBSMetaService(BaseService):

    async def get_meta_info(self, data: DBSMetaInfoRequest) -> dict:
        async with DBSMetaCollector() as c:
            return await c.get_meta_info(data.orders)

    async def delete_meta(self, data: DBSMetaDeleteRequest) -> None:
        async with DBSMetaCollector() as c:
            await c.delete_meta(data.orders, data.key)

    async def set_sgtin(self, data: DBSSetSgtinRequest) -> dict:
        async with DBSMetaCollector() as c:
            return await c.set_sgtin([o.model_dump() for o in data.orders])

    async def set_uin(self, data: DBSSetUinRequest) -> dict:
        async with DBSMetaCollector() as c:
            return await c.set_uin([o.model_dump() for o in data.orders])

    async def set_imei(self, data: DBSSetImeiRequest) -> dict:
        async with DBSMetaCollector() as c:
            return await c.set_imei([o.model_dump() for o in data.orders])

    async def set_gtin(self, data: DBSSetGtinRequest) -> dict:
        async with DBSMetaCollector() as c:
            return await c.set_gtin([o.model_dump() for o in data.orders])

    async def set_customs(self, data: DBSSetCustomsRequest) -> dict:
        async with DBSMetaCollector() as c:
            return await c.set_customs([o.model_dump() for o in data.orders])

    # --- Deprecated ---
    async def get_order_meta(self, order_id: int) -> dict:
        async with DBSMetaCollector() as c:
            return await c.get_order_meta(order_id)

    async def delete_order_meta(self, order_id: int, key: str) -> None:
        async with DBSMetaCollector() as c:
            await c.delete_order_meta(order_id, key)

    async def set_sgtin_single(self, order_id: int, data: DBSSetSgtinSingleRequest) -> dict:
        async with DBSMetaCollector() as c:
            return await c.set_sgtin_single(order_id, data.sgtins)

    async def set_uin_single(self, order_id: int, data: DBSSetUinSingleRequest) -> dict:
        async with DBSMetaCollector() as c:
            return await c.set_uin_single(order_id, data.uin)

    async def set_imei_single(self, order_id: int, data: DBSSetImeiSingleRequest) -> dict:
        async with DBSMetaCollector() as c:
            return await c.set_imei_single(order_id, data.imei)

    async def set_gtin_single(self, order_id: int, data: DBSSetGtinSingleRequest) -> dict:
        async with DBSMetaCollector() as c:
            return await c.set_gtin_single(order_id, data.gtin)

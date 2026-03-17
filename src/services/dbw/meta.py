"""Сервис: DBW — Метаданные сборочных заданий."""
from src.collectors.dbw.meta import DBWMetaCollector
from src.schemas.dbw.meta import (
    DBWOrderMetaResponse, DBWSetSgtinRequest,
    DBWSetUinRequest, DBWSetImeiRequest, DBWSetGtinRequest,
)
from src.services.base import BaseService


class DBWMetaService(BaseService):

    async def get_order_meta(self, order_id: int) -> DBWOrderMetaResponse:
        async with DBWMetaCollector() as c:
            return await c.get_order_meta(order_id)

    async def delete_order_meta(self, order_id: int, key: str) -> None:
        async with DBWMetaCollector() as c:
            await c.delete_order_meta(order_id, key)

    async def set_sgtin(self, order_id: int, data: DBWSetSgtinRequest) -> dict:
        async with DBWMetaCollector() as c:
            return await c.set_sgtin(order_id, data.sgtins)

    async def set_uin(self, order_id: int, data: DBWSetUinRequest) -> dict:
        async with DBWMetaCollector() as c:
            return await c.set_uin(order_id, data.uin)

    async def set_imei(self, order_id: int, data: DBWSetImeiRequest) -> dict:
        async with DBWMetaCollector() as c:
            return await c.set_imei(order_id, data.imei)

    async def set_gtin(self, order_id: int, data: DBWSetGtinRequest) -> dict:
        async with DBWMetaCollector() as c:
            return await c.set_gtin(order_id, data.gtin)

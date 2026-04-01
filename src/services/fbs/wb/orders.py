"""Сервис WB: FBS — Сборочные задания."""
from src.collectors.fbs.orders import OrdersCollector
from src.schemas.fbs.orders import (
    OrdersResponse, OrderStatusRequest, OrderStatusResponse,
    StickersRequest, StickersResponse, OrderMetaRequest, OrderMetaResponse,
)
from src.services.base import BaseService


class OrdersService(BaseService):

    async def get_new_orders(self) -> OrdersResponse:
        async with OrdersCollector() as c:
            return await c.get_new_orders()

    async def get_orders(self, date_from=None, date_to=None, limit=1000, offset=0) -> OrdersResponse:
        async with OrdersCollector() as c:
            return await c.get_orders(date_from=date_from, date_to=date_to, limit=limit, offset=offset)

    async def get_orders_status(self, data: OrderStatusRequest) -> OrderStatusResponse:
        async with OrdersCollector() as c:
            return await c.get_orders_status(data.orders)

    async def get_reshipment_orders(self) -> OrdersResponse:
        async with OrdersCollector() as c:
            return await c.get_reshipment_orders()

    async def cancel_order(self, order_id: int) -> None:
        async with OrdersCollector() as c:
            await c.cancel_order(order_id)

    async def get_stickers(self, data: StickersRequest, sticker_type="png", width=58, height=40) -> StickersResponse:
        async with OrdersCollector() as c:
            return await c.get_stickers(data.orders, sticker_type, width, height)

    async def get_orders_meta(self, data: OrderMetaRequest) -> OrderMetaResponse:
        async with OrdersCollector() as c:
            return await c.get_orders_meta(data.orders)

    async def delete_order_meta(self, order_id: int, key: str) -> None:
        async with OrdersCollector() as c:
            await c.delete_order_meta(order_id, key)

    async def set_order_sgtin(self, order_id: int, sgtin: str) -> dict:
        async with OrdersCollector() as c:
            return await c.set_order_sgtin(order_id, sgtin)

    async def set_order_uin(self, order_id: int, uin: str) -> dict:
        async with OrdersCollector() as c:
            return await c.set_order_uin(order_id, uin)

    async def set_order_imei(self, order_id: int, imei: str) -> dict:
        async with OrdersCollector() as c:
            return await c.set_order_imei(order_id, imei)

    async def set_order_gtin(self, order_id: int, gtin: str) -> dict:
        async with OrdersCollector() as c:
            return await c.set_order_gtin(order_id, gtin)

    async def set_order_expiration(self, order_id: int, expiration_date: str) -> dict:
        async with OrdersCollector() as c:
            return await c.set_order_expiration(order_id, expiration_date)

    async def set_order_customs(self, order_id: int, customs_number: str) -> dict:
        async with OrdersCollector() as c:
            return await c.set_order_customs(order_id, customs_number)

    async def get_crossborder_stickers(self, data: StickersRequest) -> StickersResponse:
        async with OrdersCollector() as c:
            return await c.get_crossborder_stickers(data.orders)

    async def get_status_history(self, data: OrderStatusRequest) -> dict:
        async with OrdersCollector() as c:
            return await c.get_status_history(data.orders)

    async def get_client_orders(self, order_ids: list[int]) -> dict:
        async with OrdersCollector() as c:
            return await c.get_client_orders(order_ids)

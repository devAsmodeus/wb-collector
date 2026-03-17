"""Сервис: DBS — Сборочные задания."""
from src.collectors.dbs.orders import DBSOrdersCollector
from src.schemas.dbs.orders import (
    DBSOrdersResponse, DBSOrderIdsRequest, DBSOrderStatusResponse,
    DBSDeliveryDateRequest, DBSRejectRequest, DBSReceiveRequest,
    DBSStickersResponse, DBSGroupInfoRequest,
)
from src.services.base import BaseService


class DBSOrdersService(BaseService):

    async def get_new_orders(self) -> DBSOrdersResponse:
        async with DBSOrdersCollector() as c:
            return await c.get_new_orders()

    async def get_orders(self, date_from=None, date_to=None) -> DBSOrdersResponse:
        async with DBSOrdersCollector() as c:
            return await c.get_orders(date_from=date_from, date_to=date_to)

    async def get_group_info(self, data: DBSGroupInfoRequest) -> dict:
        async with DBSOrdersCollector() as c:
            return await c.get_group_info(data.orders)

    async def get_client_orders(self, data: DBSOrderIdsRequest) -> dict:
        async with DBSOrdersCollector() as c:
            return await c.get_client_orders(data.orders)

    async def get_b2b_info(self, data: DBSOrderIdsRequest) -> dict:
        async with DBSOrdersCollector() as c:
            return await c.get_b2b_info(data.orders)

    async def set_delivery_date(self, data: DBSDeliveryDateRequest) -> None:
        async with DBSOrdersCollector() as c:
            await c.set_delivery_date(data.orders, data.deliveryDate)

    async def get_orders_status(self, data: DBSOrderIdsRequest) -> DBSOrderStatusResponse:
        async with DBSOrdersCollector() as c:
            return await c.get_orders_status(data.orders)

    async def cancel_orders(self, data: DBSOrderIdsRequest) -> None:
        async with DBSOrdersCollector() as c:
            await c.cancel_orders(data.orders)

    async def confirm_orders(self, data: DBSOrderIdsRequest) -> None:
        async with DBSOrdersCollector() as c:
            await c.confirm_orders(data.orders)

    async def get_stickers(self, data: DBSOrderIdsRequest, sticker_type="png", width=58, height=40) -> DBSStickersResponse:
        async with DBSOrdersCollector() as c:
            return await c.get_stickers(data.orders, sticker_type, width, height)

    async def deliver_orders(self, data: DBSOrderIdsRequest) -> None:
        async with DBSOrdersCollector() as c:
            await c.deliver_orders(data.orders)

    async def receive_orders(self, data: DBSReceiveRequest) -> None:
        async with DBSOrdersCollector() as c:
            await c.receive_orders(data.orders)

    async def reject_orders(self, data: DBSRejectRequest) -> None:
        async with DBSOrdersCollector() as c:
            await c.reject_orders(data.orders, data.reason)

    # --- Deprecated ---
    async def get_orders_status_deprecated(self, data: DBSOrderIdsRequest) -> DBSOrderStatusResponse:
        async with DBSOrdersCollector() as c:
            return await c.get_orders_status_deprecated(data.orders)

    async def cancel_order(self, order_id: int) -> None:
        async with DBSOrdersCollector() as c:
            await c.cancel_order(order_id)

    async def confirm_order(self, order_id: int) -> None:
        async with DBSOrdersCollector() as c:
            await c.confirm_order(order_id)

    async def deliver_order(self, order_id: int) -> None:
        async with DBSOrdersCollector() as c:
            await c.deliver_order(order_id)

    async def receive_order(self, order_id: int, payload: dict) -> None:
        async with DBSOrdersCollector() as c:
            await c.receive_order(order_id, payload)

    async def reject_order(self, order_id: int, payload: dict) -> None:
        async with DBSOrdersCollector() as c:
            await c.reject_order(order_id, payload)

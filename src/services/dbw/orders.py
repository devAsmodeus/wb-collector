"""Сервис: DBW — Сборочные задания."""
from src.collectors.dbw.orders import DBWOrdersCollector
from src.schemas.dbw.orders import (
    DBWOrdersResponse, DBWOrderStatusRequest, DBWOrderStatusResponse,
    DBWDeliveryDateRequest, DBWClientOrdersRequest,
    DBWStickersRequest, DBWStickersResponse, DBWCourierRequest,
)
from src.services.base import BaseService


class DBWOrdersService(BaseService):

    async def get_new_orders(self) -> DBWOrdersResponse:
        async with DBWOrdersCollector() as c:
            return await c.get_new_orders()

    async def get_orders(self, date_from=None, date_to=None) -> DBWOrdersResponse:
        async with DBWOrdersCollector() as c:
            return await c.get_orders(date_from=date_from, date_to=date_to)

    async def set_delivery_date(self, data: DBWDeliveryDateRequest) -> None:
        async with DBWOrdersCollector() as c:
            await c.set_delivery_date(data.orders, data.deliveryDate)

    async def get_client_orders(self, data: DBWClientOrdersRequest) -> dict:
        async with DBWOrdersCollector() as c:
            return await c.get_client_orders(data.orders)

    async def get_orders_status(self, data: DBWOrderStatusRequest) -> DBWOrderStatusResponse:
        async with DBWOrdersCollector() as c:
            return await c.get_orders_status(data.orders)

    async def confirm_order(self, order_id: int) -> None:
        async with DBWOrdersCollector() as c:
            await c.confirm_order(order_id)

    async def get_stickers(self, data: DBWStickersRequest, sticker_type="png", width=58, height=40) -> DBWStickersResponse:
        async with DBWOrdersCollector() as c:
            return await c.get_stickers(data.orders, sticker_type, width, height)

    async def assemble_order(self, order_id: int) -> None:
        async with DBWOrdersCollector() as c:
            await c.assemble_order(order_id)

    async def call_courier(self, data: DBWCourierRequest) -> None:
        async with DBWOrdersCollector() as c:
            await c.call_courier(data.orders)

    async def cancel_order(self, order_id: int) -> None:
        async with DBWOrdersCollector() as c:
            await c.cancel_order(order_id)

"""Сервис: Самовывоз — Сборочные задания."""
from src.collectors.pickup.orders import PickupOrdersCollector
from src.schemas.pickup.orders import (
    PickupOrdersResponse, PickupOrderIdsRequest, PickupOrderStatusResponse,
    PickupRejectRequest, PickupReceiveRequest,
)
from src.services.base import BaseService


class PickupOrdersService(BaseService):

    async def get_new_orders(self) -> PickupOrdersResponse:
        async with PickupOrdersCollector() as c:
            return await c.get_new_orders()

    async def confirm_orders(self, data: PickupOrderIdsRequest) -> None:
        async with PickupOrdersCollector() as c:
            await c.confirm_orders(data.orders)

    async def prepare_orders(self, data: PickupOrderIdsRequest) -> None:
        async with PickupOrdersCollector() as c:
            await c.prepare_orders(data.orders)

    async def get_client_orders(self, data: PickupOrderIdsRequest) -> dict:
        async with PickupOrdersCollector() as c:
            return await c.get_client_orders(data.orders)

    async def get_client_identity(self, data: PickupOrderIdsRequest) -> dict:
        async with PickupOrdersCollector() as c:
            return await c.get_client_identity(data.orders)

    async def receive_orders(self, data: PickupReceiveRequest) -> None:
        async with PickupOrdersCollector() as c:
            await c.receive_orders(data.orders)

    async def reject_orders(self, data: PickupRejectRequest) -> None:
        async with PickupOrdersCollector() as c:
            await c.reject_orders(data.orders, data.reason)

    async def get_orders_status(self, data: PickupOrderIdsRequest) -> PickupOrderStatusResponse:
        async with PickupOrdersCollector() as c:
            return await c.get_orders_status(data.orders)

    async def get_orders(self, date_from=None, date_to=None) -> PickupOrdersResponse:
        async with PickupOrdersCollector() as c:
            return await c.get_orders(date_from=date_from, date_to=date_to)

    async def cancel_orders(self, data: PickupOrderIdsRequest) -> None:
        async with PickupOrdersCollector() as c:
            await c.cancel_orders(data.orders)

    # --- Deprecated ---
    async def confirm_order(self, order_id: int) -> None:
        async with PickupOrdersCollector() as c:
            await c.confirm_order(order_id)

    async def prepare_order(self, order_id: int) -> None:
        async with PickupOrdersCollector() as c:
            await c.prepare_order(order_id)

    async def receive_order(self, order_id: int) -> None:
        async with PickupOrdersCollector() as c:
            await c.receive_order(order_id)

    async def reject_order(self, order_id: int, payload: dict) -> None:
        async with PickupOrdersCollector() as c:
            await c.reject_order(order_id, payload)

    async def get_orders_status_deprecated(self, data: PickupOrderIdsRequest) -> PickupOrderStatusResponse:
        async with PickupOrdersCollector() as c:
            return await c.get_orders_status_deprecated(data.orders)

    async def cancel_order(self, order_id: int) -> None:
        async with PickupOrdersCollector() as c:
            await c.cancel_order(order_id)

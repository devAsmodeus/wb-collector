"""Сервис: FBS — Поставки и короба."""
from src.collectors.fbs.supplies import SuppliesCollector
from src.schemas.fbs.supplies import (
    SuppliesResponse, CreateSupplyRequest, CreateSupplyResponse,
    SupplyOrderIdsResponse, SupplyBarcode,
    BoxesResponse, AddOrdersToSupplyRequest,
    AddBoxesRequest, DeleteBoxesRequest,
    BoxStickersRequest, BoxStickersResponse,
)
from src.services.base import BaseService


class SuppliesService(BaseService):

    async def create_supply(self, data: CreateSupplyRequest) -> CreateSupplyResponse:
        async with SuppliesCollector() as c:
            return await c.create_supply(data.name)

    async def get_supplies(self, limit=1000, offset=0) -> SuppliesResponse:
        async with SuppliesCollector() as c:
            return await c.get_supplies(limit=limit, offset=offset)

    async def get_supply(self, supply_id: str) -> dict:
        async with SuppliesCollector() as c:
            return await c.get_supply(supply_id)

    async def delete_supply(self, supply_id: str) -> None:
        async with SuppliesCollector() as c:
            await c.delete_supply(supply_id)

    async def add_orders_to_supply(self, supply_id: str, data: AddOrdersToSupplyRequest) -> None:
        async with SuppliesCollector() as c:
            await c.add_orders_to_supply(supply_id, data.orders)

    async def get_supply_order_ids(self, supply_id: str) -> SupplyOrderIdsResponse:
        async with SuppliesCollector() as c:
            return await c.get_supply_order_ids(supply_id)

    async def deliver_supply(self, supply_id: str) -> None:
        async with SuppliesCollector() as c:
            await c.deliver_supply(supply_id)

    async def get_supply_barcode(self, supply_id: str, barcode_type: str = "svg") -> SupplyBarcode:
        async with SuppliesCollector() as c:
            return await c.get_supply_barcode(supply_id, barcode_type)

    async def get_supply_boxes(self, supply_id: str) -> BoxesResponse:
        async with SuppliesCollector() as c:
            return await c.get_supply_boxes(supply_id)

    async def add_boxes(self, supply_id: str, data: AddBoxesRequest) -> BoxesResponse:
        async with SuppliesCollector() as c:
            return await c.add_boxes(supply_id, data.quantity)

    async def delete_boxes(self, supply_id: str, data: DeleteBoxesRequest) -> None:
        async with SuppliesCollector() as c:
            await c.delete_boxes(supply_id, data.trbx)

    async def get_box_stickers(self, supply_id: str, data: BoxStickersRequest, sticker_type="png") -> BoxStickersResponse:
        async with SuppliesCollector() as c:
            return await c.get_box_stickers(supply_id, data.trbx, sticker_type)

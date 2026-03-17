"""Сервис: FBW — Информация о поставках."""
from src.collectors.fbw.supplies import FBWSuppliesCollector
from src.schemas.fbw.supplies import (
    FBWSuppliesFiltersRequest, FBWSuppliesResponse,
    FBWSupplyGoodsResponse, FBWPackageQR,
)
from src.services.base import BaseService


class FBWSuppliesService(BaseService):

    async def get_supplies(
        self, data: FBWSuppliesFiltersRequest, limit: int = 1000, offset: int = 0
    ) -> FBWSuppliesResponse:
        async with FBWSuppliesCollector() as c:
            return await c.get_supplies(data.model_dump(exclude_none=True), limit, offset)

    async def get_supply(self, supply_id: int, is_preorder_id: bool = False) -> dict:
        async with FBWSuppliesCollector() as c:
            return await c.get_supply(supply_id, is_preorder_id)

    async def get_supply_goods(
        self, supply_id: int, limit: int = 1000, offset: int = 0, is_preorder_id: bool = False
    ) -> FBWSupplyGoodsResponse:
        async with FBWSuppliesCollector() as c:
            return await c.get_supply_goods(supply_id, limit, offset, is_preorder_id)

    async def get_supply_package(self, supply_id: int) -> FBWPackageQR:
        async with FBWSuppliesCollector() as c:
            return await c.get_supply_package(supply_id)

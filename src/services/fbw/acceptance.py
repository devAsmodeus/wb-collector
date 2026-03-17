"""Сервис: FBW — Информация для формирования поставок."""
from src.collectors.fbw.acceptance import FBWAcceptanceCollector
from src.schemas.fbw.acceptance import (
    FBWAcceptanceOptionsRequest, FBWWarehousesResponse, FBWTransitTariffsResponse,
)
from src.services.base import BaseService


class FBWAcceptanceService(BaseService):

    async def get_acceptance_options(
        self, data: FBWAcceptanceOptionsRequest, warehouse_id: int | None = None
    ) -> dict:
        async with FBWAcceptanceCollector() as c:
            goods = [item.model_dump() for item in data.goods]
            return await c.get_acceptance_options(goods, warehouse_id)

    async def get_warehouses(self) -> FBWWarehousesResponse:
        async with FBWAcceptanceCollector() as c:
            return await c.get_warehouses()

    async def get_transit_tariffs(self) -> FBWTransitTariffsResponse:
        async with FBWAcceptanceCollector() as c:
            return await c.get_transit_tariffs()

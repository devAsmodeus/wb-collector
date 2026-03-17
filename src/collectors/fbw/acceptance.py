"""Коллектор: FBW — Информация для формирования поставок."""
from src.collectors.base import WBApiClient
from src.config import settings
from src.schemas.fbw.acceptance import FBWWarehousesResponse, FBWTransitTariffsResponse


class FBWAcceptanceCollector:
    def __init__(self):
        self._client = WBApiClient(base_url=settings.WB_MARKETPLACE_URL, token=settings.WB_API_TOKEN)

    async def __aenter__(self):
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self._client.__aexit__(*args)

    async def get_acceptance_options(self, goods: list[dict], warehouse_id: int | None = None) -> dict:
        """POST /api/v1/acceptance/options — опции приёмки для списка товаров."""
        params = {}
        if warehouse_id:
            params["warehouseID"] = warehouse_id
        return await self._client.post("/api/v1/acceptance/options", json=goods, params=params)

    async def get_warehouses(self) -> FBWWarehousesResponse:
        """GET /api/v1/warehouses — список складов WB."""
        data = await self._client.get("/api/v1/warehouses")
        return FBWWarehousesResponse.model_validate(
            data if isinstance(data, dict) else {"warehouses": data or []}
        )

    async def get_transit_tariffs(self) -> FBWTransitTariffsResponse:
        """GET /api/v1/transit-tariffs — тарифы транзитной доставки."""
        data = await self._client.get("/api/v1/transit-tariffs")
        return FBWTransitTariffsResponse.model_validate(
            data if isinstance(data, dict) else {"tariffs": data or []}
        )

"""Коллектор: Тарифы WB."""
from src.collectors.base import WBApiClient
from src.config import settings
from src.schemas.tariffs.tariffs import (
    CommissionsResponse,
    ReturnCostResponse,
    BoxTariffsResponse,
    PalletTariffsResponse,
    SupplyTariffItem,
)


class TariffsCollector:
    def __init__(self):
        self._client = WBApiClient(base_url=settings.WB_COMMON_URL, token=settings.WB_API_TOKEN)

    async def __aenter__(self):
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self._client.__aexit__(*args)

    async def get_commissions(self) -> CommissionsResponse:
        data = await self._client.get("/api/v1/tariffs/commission")
        return CommissionsResponse.model_validate(data if isinstance(data, dict) else {"report": data})

    async def get_return_cost(self, date: str | None = None) -> ReturnCostResponse:
        params = {}
        if date:
            params["date"] = date
        data = await self._client.get("/api/v1/tariffs/return", params=params)
        # WB wraps: {"response": {"data": {dtNextBox, dtTillMax, warehouseList}}}
        inner = data.get("response", {}).get("data", data) if isinstance(data, dict) else data
        return ReturnCostResponse.model_validate(inner if isinstance(inner, dict) else {})

    async def get_box_tariffs(self, date: str | None = None) -> BoxTariffsResponse:
        params = {}
        if date:
            params["date"] = date
        data = await self._client.get("/api/v1/tariffs/box", params=params)
        # WB wraps: {"response": {"data": {dtNextBox, dtTillMax, warehouseList}}}
        inner = data.get("response", {}).get("data", data) if isinstance(data, dict) else data
        return BoxTariffsResponse.model_validate(inner if isinstance(inner, dict) else {})

    async def get_pallet_tariffs(self, date: str | None = None) -> PalletTariffsResponse:
        params = {}
        if date:
            params["date"] = date
        data = await self._client.get("/api/v1/tariffs/pallet", params=params)
        # WB wraps: {"response": {"data": {dtNextBox, dtTillMax, warehouseList}}}
        inner = data.get("response", {}).get("data", data) if isinstance(data, dict) else data
        return PalletTariffsResponse.model_validate(inner if isinstance(inner, dict) else {})

    async def get_supply_tariffs(self, warehouse_ids: str | None = None) -> list[SupplyTariffItem]:
        """GET /api/tariffs/v1/acceptance/coefficients — коэффициенты приёмки."""
        params = {}
        if warehouse_ids:
            params["warehouseIDs"] = warehouse_ids
        data = await self._client.get("/api/tariffs/v1/acceptance/coefficients", params=params)
        items = data if isinstance(data, list) else []
        return [SupplyTariffItem.model_validate(item) for item in items]

"""Коллектор: Тарифы WB."""
from src.collectors.base import WBApiClient
from src.config import settings


class TariffsCollector:
    def __init__(self):
        self._client = WBApiClient(base_url=settings.WB_COMMON_URL, token=settings.WB_API_TOKEN)

    async def __aenter__(self):
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self._client.__aexit__(*args)

    async def get_commissions(self) -> dict:
        return await self._client.get("/api/v1/tariffs/commission")

    async def get_return_cost(self, date: str | None = None) -> dict:
        params = {}
        if date:
            params["date"] = date
        return await self._client.get("/api/v1/tariffs/seller", params=params)

    async def get_box_tariffs(self, date: str | None = None) -> dict:
        params = {}
        if date:
            params["date"] = date
        return await self._client.get("/api/v1/tariffs/box", params=params)

    async def get_pallet_tariffs(self, date: str | None = None) -> dict:
        params = {}
        if date:
            params["date"] = date
        return await self._client.get("/api/v1/tariffs/pallet", params=params)

    async def get_supply_tariffs(self, date: str | None = None) -> dict:
        params = {}
        if date:
            params["date"] = date
        return await self._client.get("/api/v1/tariffs/warehouseCoeff", params=params)

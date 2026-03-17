"""Коллектор: Маркетинг — Поисковые кластеры."""
from src.collectors.base import WBApiClient
from src.config import settings


class SearchCollector:
    def __init__(self):
        self._client = WBApiClient(base_url=settings.WB_ADVERT_URL, token=settings.WB_API_TOKEN)

    async def __aenter__(self):
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self._client.__aexit__(*args)

    async def get_normquery_stats(self, payload: dict) -> dict:
        return await self._client.post("/adv/v0/normquery/stats", json=payload)

    async def get_normquery_bids(self, payload: dict) -> dict:
        return await self._client.post("/adv/v0/normquery/get-bids", json=payload)

    async def set_normquery_bids(self, payload: dict) -> dict:
        return await self._client.post("/adv/v0/normquery/bids", json=payload)

    async def delete_normquery_bids(self, payload: dict) -> dict:
        return await self._client.delete("/adv/v0/normquery/bids", json=payload)

    async def get_normquery_minus(self, payload: dict) -> dict:
        return await self._client.post("/adv/v0/normquery/get-minus", json=payload)

    async def set_normquery_minus(self, payload: dict) -> dict:
        return await self._client.post("/adv/v0/normquery/set-minus", json=payload)

    async def get_normquery_list(self, payload: dict) -> dict:
        return await self._client.post("/adv/v0/normquery/list", json=payload)

    async def get_normquery_stats_v1(self, payload: dict) -> dict:
        return await self._client.post("/adv/v1/normquery/stats", json=payload)

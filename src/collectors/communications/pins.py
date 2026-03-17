"""Коллектор: Коммуникации — Закреплённые отзывы."""
from src.collectors.base import WBApiClient
from src.config import settings


class PinsCollector:
    def __init__(self):
        self._client = WBApiClient(base_url=settings.WB_FEEDBACKS_URL, token=settings.WB_API_TOKEN)

    async def __aenter__(self):
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self._client.__aexit__(*args)

    async def get_list(self, nm_id: int | None = None) -> dict:
        params: dict = {}
        if nm_id: params["nmId"] = nm_id
        return await self._client.get("/api/feedbacks/v1/pins", params=params)

    async def pin(self, payload: dict) -> dict:
        return await self._client.post("/api/feedbacks/v1/pins", json=payload)

    async def unpin(self, payload: dict) -> dict:
        return await self._client.delete("/api/feedbacks/v1/pins", json=payload)

    async def get_count(self) -> dict:
        return await self._client.get("/api/feedbacks/v1/pins/count")

    async def get_limits(self) -> dict:
        return await self._client.get("/api/feedbacks/v1/pins/limits")

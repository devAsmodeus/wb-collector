"""Коллектор: Коммуникации — Претензии."""
from src.collectors.base import WBApiClient
from src.config import settings


class ClaimsCollector:
    def __init__(self):
        self._client = WBApiClient(base_url=settings.WB_FEEDBACKS_URL, token=settings.WB_API_TOKEN)

    async def __aenter__(self):
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self._client.__aexit__(*args)

    async def get_claims(self, limit: int = 10, offset: int = 0) -> dict:
        return await self._client.get("/api/v1/claims", params={"take": limit, "skip": offset})

    async def update_claim(self, payload: dict) -> dict:
        return await self._client.patch("/api/v1/claim", json=payload)

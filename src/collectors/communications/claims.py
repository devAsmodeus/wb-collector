"""Коллектор: Коммуникации — Претензии.

YAML: docs/api/09-communications.yaml
Host: returns-api.wildberries.ru (НЕ feedbacks-api!)
Параметры: limit/offset (НЕ take/skip!)
"""
from src.collectors.base import WBApiClient
from src.config import settings


class ClaimsCollector:
    def __init__(self):
        self._client = WBApiClient(base_url=settings.WB_RETURNS_URL, token=settings.WB_API_TOKEN)

    async def __aenter__(self):
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self._client.__aexit__(*args)

    async def get_claims(
        self,
        limit: int = 10,
        offset: int = 0,
        is_archive: bool | None = None,
        claim_id: str | None = None,
        nm_id: int | None = None,
    ) -> dict:
        """GET /api/v1/claims — претензии (последние 14 дней)."""
        params: dict = {"limit": limit, "offset": offset}
        if is_archive is not None:
            params["is_archive"] = str(is_archive).lower()
        if claim_id:
            params["id"] = claim_id
        if nm_id:
            params["nm_id"] = nm_id
        return await self._client.get("/api/v1/claims", params=params)

    async def update_claim(self, payload: dict) -> dict:
        return await self._client.patch("/api/v1/claim", json=payload)

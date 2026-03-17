"""Коллектор: Маркетинг — Финансы."""
from src.collectors.base import WBApiClient
from src.config import settings


class FinanceCollector:
    def __init__(self):
        self._client = WBApiClient(base_url=settings.WB_ADVERT_URL, token=settings.WB_API_TOKEN)

    async def __aenter__(self):
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self._client.__aexit__(*args)

    async def get_balance(self) -> dict:
        return await self._client.get("/adv/v1/balance")

    async def get_budget(self, advert_id: int) -> dict:
        return await self._client.get("/adv/v1/budget", params={"id": advert_id})

    async def deposit_budget(self, advert_id: int, payload: dict) -> dict:
        return await self._client.post("/adv/v1/budget/deposit", json=payload, params={"id": advert_id})

    async def get_upd(self, date_from: str, date_to: str) -> dict:
        return await self._client.get("/adv/v1/upd", params={"from": date_from, "to": date_to})

    async def get_payments(self, date_from: str, date_to: str) -> dict:
        return await self._client.get("/adv/v1/payments", params={"from": date_from, "to": date_to})

"""Коллектор: Коммуникации — Чат с покупателями."""
from src.collectors.base import WBApiClient
from src.config import settings


class ChatCollector:
    def __init__(self):
        self._client = WBApiClient(base_url=settings.WB_BUYER_CHAT_URL, token=settings.WB_API_TOKEN)

    async def __aenter__(self):
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self._client.__aexit__(*args)

    async def get_chats(self, limit: int = 10, offset: int = 0) -> dict:
        return await self._client.get("/api/v1/seller/chats", params={"take": limit, "skip": offset})

    async def get_events(self, chat_id: str, limit: int = 10, offset: int = 0) -> dict:
        return await self._client.get(
            "/api/v1/seller/events",
            params={"chatId": chat_id, "take": limit, "skip": offset},
        )

    async def send_message(self, payload: dict) -> dict:
        return await self._client.post("/api/v1/seller/message", json=payload)

    async def download_file(self, file_id: str) -> dict:
        return await self._client.get(f"/api/v1/seller/download/{file_id}")

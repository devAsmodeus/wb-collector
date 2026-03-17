"""Коллектор: Коммуникации — Новые вопросы/отзывы."""
from src.collectors.base import WBApiClient
from src.config import settings


class NewItemsCollector:
    def __init__(self):
        self._client = WBApiClient(base_url=settings.WB_FEEDBACKS_URL, token=settings.WB_API_TOKEN)

    async def __aenter__(self):
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self._client.__aexit__(*args)

    async def get_new_feedbacks_questions(self) -> dict:
        return await self._client.get("/api/v1/new-feedbacks-questions")

"""Сервис: Общее — АПИ новостей."""
from src.collectors.general.news import NewsCollector
from src.schemas.general.news import NewsResponse
from src.services.base import BaseService


class NewsService(BaseService):

    async def get_news(
        self,
        from_date: str | None = None,
        from_id: int | None = None,
    ) -> NewsResponse:
        async with NewsCollector() as c:
            return await c.get_news(from_date=from_date, from_id=from_id)

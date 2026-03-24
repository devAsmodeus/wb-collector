"""Сервис WB: Общее — Новости."""
from src.collectors.general.news import NewsCollector
from src.schemas.general.news import NewsResponse
from src.services.base import BaseService


class NewsWbService(BaseService):

    async def get_news(
        self,
        from_date: str | None = None,
        from_id: int | None = None,
    ) -> NewsResponse:
        """Проксирует запрос к WB API без сохранения в БД."""
        async with NewsCollector() as c:
            return await c.get_news(from_date=from_date, from_id=from_id)

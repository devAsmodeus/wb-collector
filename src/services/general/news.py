"""Сервис: Общее — АПИ новостей."""
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.general.news import NewsCollector
from src.repositories.news import NewsRepository
from src.schemas.general.news import NewsResponse
from src.services.base import BaseService


class NewsService(BaseService):

    async def get_news(
        self,
        from_date: str | None = None,
        from_id: int | None = None,
    ) -> NewsResponse:
        """Проксирует запрос к WB API без сохранения в БД."""
        async with NewsCollector() as c:
            return await c.get_news(from_date=from_date, from_id=from_id)

    async def sync_all(self, session: AsyncSession) -> dict:
        """
        Полная выгрузка новостей за всё время.
        WB API не поддерживает пагинацию — возвращает все новости за указанный период.
        Берём данные с 2020-01-01 (старт WB Seller API).
        """
        repo = NewsRepository(session)
        async with NewsCollector() as c:
            response = await c.get_news(from_date="2020-01-01")
        saved = await repo.upsert_many(response.data)
        return {"synced": saved, "source": "full", "from_date": "2020-01-01"}

    async def sync_incremental(self, session: AsyncSession) -> dict:
        """
        Инкрементальная синхронизация — только новые новости начиная с max news_id в БД.
        Если БД пуста — делает полную выгрузку.
        """
        repo = NewsRepository(session)
        max_id = await repo.get_max_id()

        async with NewsCollector() as c:
            if max_id:
                response = await c.get_news(from_id=max_id)
            else:
                # БД пуста — полный импорт
                response = await c.get_news(from_date="2020-01-01")

        saved = await repo.upsert_many(response.data)
        return {
            "synced": saved,
            "source": "incremental" if max_id else "full",
            "from_id": max_id,
        }

    async def get_from_db(self, session: AsyncSession, limit: int = 100, offset: int = 0) -> dict:
        """Возвращает новости из БД."""
        repo = NewsRepository(session)
        items = await repo.get_all(limit=limit, offset=offset)
        return {
            "data": [
                {
                    "news_id": n.news_id,
                    "header": n.header,
                    "content": n.content,
                    "date": n.date.isoformat() if n.date else None,
                    "types": n.types,
                }
                for n in items
            ],
            "count": len(items),
        }

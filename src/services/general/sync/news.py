"""Сервис Sync: Общее — Синхронизация новостей."""
import logging
from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.general.news import NewsCollector
from src.repositories.general.news import NewsRepository
from src.services.base import BaseService

logger = logging.getLogger(__name__)

_PAGE_SIZE = 100  # WB API: не более 100 новостей за запрос


class NewsSyncService(BaseService):

    async def sync_all(self, session: AsyncSession) -> dict:
        """
        Полная выгрузка всех новостей с пагинацией через fromID.
        WB API: max 100 за запрос, пагинация через fromID (следующий ID после последнего полученного).
        Лимит: 1 req/min (burst 10), поэтому большое кол-во страниц — редкость.
        """
        repo = NewsRepository(session)
        total_saved = 0

        async with NewsCollector() as c:
            # Первый запрос — с начала времён
            response = await c.get_news(from_date="2018-01-01")
            items = response.data or []

            while items:
                saved = await repo.upsert_many(items)
                total_saved += saved
                logger.info(f"News sync: got {len(items)}, saved {saved}, total={total_saved}")

                if len(items) < _PAGE_SIZE:
                    break  # Последняя страница

                # Следующая страница — с ID после последнего
                max_id = max(item.id for item in items if item.id)
                response = await c.get_news(from_id=max_id + 1)
                items = response.data or []

        logger.info(f"News full sync done: {total_saved} total")
        return {"synced": total_saved, "source": "full"}

    # Алиас для Celery-задачи sync.general.news_full
    async def sync_news_full(self, session: AsyncSession) -> dict:
        return await self.sync_all(session)

    async def sync_incremental(self, session: AsyncSession) -> dict:
        """
        Инкрементальная синхронизация — только новые новости начиная с max news_id в БД.
        Если БД пуста — выполняет полную выгрузку.
        """
        repo = NewsRepository(session)
        max_id = await repo.get_max_id()

        if not max_id:
            logger.info("News incremental: DB empty, running full sync")
            result = await self.sync_all(session)
            result["source"] = "incremental_fallback_full"
            return result

        total_saved = 0
        async with NewsCollector() as c:
            response = await c.get_news(from_id=max_id + 1)
            items = response.data or []

            while items:
                saved = await repo.upsert_many(items)
                total_saved += saved
                logger.info(f"News incremental: got {len(items)}, saved {saved}")

                if len(items) < _PAGE_SIZE:
                    break

                max_id = max(item.id for item in items if item.id)
                response = await c.get_news(from_id=max_id + 1)
                items = response.data or []

        return {
            "synced": total_saved,
            "source": "incremental",
            "from_id": max_id,
        }

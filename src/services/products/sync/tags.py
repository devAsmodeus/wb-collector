"""Сервис Sync: Товары — Синхронизация тегов."""
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.products import ProductsCollector
from src.repositories.products.tags import TagsRepository
from src.services.base import BaseService

logger = logging.getLogger(__name__)


class TagsSyncService(BaseService):

    async def sync_tags(self, session: AsyncSession) -> dict:
        """Полная выгрузка всех тегов продавца."""
        repo = TagsRepository(session)

        async with ProductsCollector() as collector:
            response = await collector.tags.get_tags()

        tags = response.data if response.data else []
        saved = await repo.upsert_many(tags)
        logger.info(f"Tags synced: {saved} tags saved")
        return {"synced": saved, "source": "full"}

    async def sync_tags_incremental(self, session: AsyncSession) -> dict:
        """
        Инкрементальная синхронизация тегов.
        Теги — справочные данные, incremental = full sync.
        """
        result = await self.sync_tags(session)
        result["source"] = "incremental"
        return result

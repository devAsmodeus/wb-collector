"""Сервис Sync: Товары — Синхронизация справочников (категории, предметы)."""
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.products import ProductsCollector
from src.repositories.products.categories import CategoriesRepository
from src.repositories.products.subjects import SubjectsRepository
from src.services.base import BaseService

logger = logging.getLogger(__name__)


class DirectoriesSyncService(BaseService):

    async def sync_categories(self, session: AsyncSession) -> dict:
        """Полная выгрузка родительских категорий товаров."""
        repo = CategoriesRepository(session)

        async with ProductsCollector() as collector:
            response = await collector.directories.get_parent_categories()

        categories = [
            {"category_id": cat.id, "name": cat.name}
            for cat in (response.data if response.data else [])
            if cat.id is not None
        ]
        saved = await repo.upsert_many(categories)
        logger.info(f"Categories synced: {saved} categories saved")
        return {"synced": saved, "source": "full"}

    async def sync_subjects(self, session: AsyncSession) -> dict:
        """Полная выгрузка предметов (подкатегорий) товаров."""
        repo = SubjectsRepository(session)

        async with ProductsCollector() as collector:
            response = await collector.directories.get_subjects(limit=1000)

        subjects = [
            {
                "subject_id": subj.subjectID,
                "name": subj.subjectName,
                "parent_id": subj.parentID,
            }
            for subj in (response.data if response.data else [])
        ]
        saved = await repo.upsert_many(subjects)
        logger.info(f"Subjects synced: {saved} subjects saved")
        return {"synced": saved, "source": "full"}

    async def sync_categories_incremental(self, session: AsyncSession) -> dict:
        """
        Инкрементальная синхронизация категорий.
        Категории — справочные данные, incremental = full sync.
        """
        result = await self.sync_categories(session)
        result["source"] = "incremental"
        return result

    async def sync_subjects_incremental(self, session: AsyncSession) -> dict:
        """
        Инкрементальная синхронизация предметов.
        Предметы — справочные данные, incremental = full sync.
        """
        result = await self.sync_subjects(session)
        result["source"] = "incremental"
        return result

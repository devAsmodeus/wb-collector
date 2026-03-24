"""Сервис DB: Товары — Чтение справочников из БД."""
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.products.categories import CategoriesRepository
from src.repositories.products.subjects import SubjectsRepository
from src.services.base import BaseService


class DirectoriesDbService(BaseService):

    async def get_categories(self, session: AsyncSession) -> dict:
        """Возвращает все категории из БД."""
        repo = CategoriesRepository(session)
        items = await repo.get_all()
        return {
            "data": [
                {
                    "category_id": c.category_id,
                    "name": c.name,
                    "parent_id": c.parent_id,
                    "fetched_at": c.fetched_at.isoformat() if c.fetched_at else None,
                }
                for c in items
            ],
            "count": len(items),
        }

    async def get_subjects(self, session: AsyncSession) -> dict:
        """Возвращает все предметы из БД."""
        repo = SubjectsRepository(session)
        items = await repo.get_all()
        return {
            "data": [
                {
                    "subject_id": s.subject_id,
                    "name": s.name,
                    "parent_id": s.parent_id,
                    "fetched_at": s.fetched_at.isoformat() if s.fetched_at else None,
                }
                for s in items
            ],
            "count": len(items),
        }

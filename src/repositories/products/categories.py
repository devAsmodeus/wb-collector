"""Репозиторий: Категории товаров WB."""
from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.products import WbCategory


class CategoriesRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def upsert_many(self, categories: list[dict]) -> int:
        """Вставляет или обновляет категории. Возвращает кол-во обработанных записей.

        Каждый dict должен содержать ключи: category_id, name, parent_id (опционально).
        """
        if not categories:
            return 0
        rows = [
            {
                "category_id": cat["category_id"],
                "name": cat["name"],
                "parent_id": cat.get("parent_id"),
                "fetched_at": datetime.utcnow(),
            }
            for cat in categories
        ]
        stmt = insert(WbCategory).values(rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=["category_id"],
            set_={
                "name": stmt.excluded.name,
                "parent_id": stmt.excluded.parent_id,
                "fetched_at": stmt.excluded.fetched_at,
            },
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return len(rows)

    async def count(self) -> int:
        """Возвращает общее количество категорий в БД."""
        result = await self._session.execute(select(func.count()).select_from(WbCategory))
        return result.scalar_one()

    async def get_all(self) -> list[WbCategory]:
        """Возвращает все категории."""
        result = await self._session.execute(
            select(WbCategory).order_by(WbCategory.category_id)
        )
        return list(result.scalars().all())

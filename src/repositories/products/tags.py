"""Репозиторий: Теги карточек товаров."""
from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.products import WbTag
from src.schemas.products.tags import WBTag


class TagsRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def upsert_many(self, tags: list[WBTag]) -> int:
        """Вставляет или обновляет теги. Возвращает кол-во обработанных записей."""
        if not tags:
            return 0
        rows = [
            {
                "tag_id": tag.id,
                "name": tag.name,
                "color": tag.color,
                "fetched_at": datetime.utcnow(),
            }
            for tag in tags
        ]
        stmt = insert(WbTag).values(rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=["tag_id"],
            set_={
                "name": stmt.excluded.name,
                "color": stmt.excluded.color,
                "fetched_at": stmt.excluded.fetched_at,
            },
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return len(rows)

    async def count(self) -> int:
        """Возвращает общее количество тегов в БД."""
        result = await self._session.execute(select(func.count()).select_from(WbTag))
        return result.scalar_one()

    async def get_all(self) -> list[WbTag]:
        """Возвращает все теги."""
        result = await self._session.execute(
            select(WbTag).order_by(WbTag.tag_id)
        )
        return list(result.scalars().all())

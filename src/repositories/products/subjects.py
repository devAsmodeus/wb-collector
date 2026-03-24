"""Репозиторий: Предметы (подкатегории) товаров WB."""
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.products import WbSubject


class SubjectsRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def upsert_many(self, subjects: list[dict]) -> int:
        """Вставляет или обновляет предметы. Возвращает кол-во обработанных записей.

        Каждый dict должен содержать ключи: subject_id, name, parent_id (опционально).
        """
        if not subjects:
            return 0
        rows = [
            {
                "subject_id": subj["subject_id"],
                "name": subj["name"],
                "parent_id": subj.get("parent_id"),
                "fetched_at": datetime.utcnow(),
            }
            for subj in subjects
        ]
        stmt = insert(WbSubject).values(rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=["subject_id"],
            set_={
                "name": stmt.excluded.name,
                "parent_id": stmt.excluded.parent_id,
                "fetched_at": stmt.excluded.fetched_at,
            },
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return len(rows)

    async def get_all(self) -> list[WbSubject]:
        """Возвращает все предметы."""
        result = await self._session.execute(
            select(WbSubject).order_by(WbSubject.subject_id)
        )
        return list(result.scalars().all())

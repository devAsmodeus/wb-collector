"""Репозиторий: Вопросы покупателей."""
from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.communications import WbQuestion


class QuestionsRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def upsert_many(self, questions: list[dict]) -> int:
        """Вставляет или обновляет вопросы. Возвращает кол-во обработанных записей."""
        if not questions:
            return 0
        rows = [
            {
                "question_id": q.get("id", ""),
                "created_date": datetime.fromisoformat(q["createdDate"]) if q.get("createdDate") else None,
                "state": q.get("state"),
                "text": q.get("text"),
                "nm_id": q.get("nmId"),
                "answer_text": q.get("answer", {}).get("text") if q.get("answer") else None,
                "user_name": q.get("userName"),
                "product_details": q.get("productDetails"),
                "fetched_at": datetime.utcnow(),
            }
            for q in questions
        ]
        stmt = insert(WbQuestion).values(rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=["question_id"],
            set_={
                "created_date": stmt.excluded.created_date,
                "state": stmt.excluded.state,
                "text": stmt.excluded.text,
                "nm_id": stmt.excluded.nm_id,
                "answer_text": stmt.excluded.answer_text,
                "user_name": stmt.excluded.user_name,
                "product_details": stmt.excluded.product_details,
                "fetched_at": stmt.excluded.fetched_at,
            },
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return len(rows)

    async def get_max_date(self) -> datetime | None:
        """Возвращает максимальную дату создания вопроса из БД для инкрементальной синхронизации."""
        result = await self._session.execute(select(func.max(WbQuestion.created_date)))
        return result.scalar_one_or_none()

    async def count(self) -> int:
        """Возвращает общее количество вопросов в БД."""
        result = await self._session.execute(select(func.count()).select_from(WbQuestion))
        return result.scalar_one()

    async def get_all(self, limit: int = 100, offset: int = 0) -> list[WbQuestion]:
        """Возвращает вопросы из БД (последние сначала)."""
        result = await self._session.execute(
            select(WbQuestion).order_by(WbQuestion.created_date.desc()).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def get_filtered(
        self,
        date_from: str | None = None,
        date_to: str | None = None,
        is_answered: bool | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[WbQuestion]:
        """Возвращает вопросы с фильтрацией по параметрам."""
        query = select(WbQuestion)
        if date_from:
            query = query.where(WbQuestion.created_date >= datetime.fromisoformat(date_from))
        if date_to:
            query = query.where(WbQuestion.created_date <= datetime.fromisoformat(date_to))
        if is_answered is not None:
            if is_answered:
                query = query.where(WbQuestion.answer_text.isnot(None))
            else:
                query = query.where(WbQuestion.answer_text.is_(None))
        query = query.order_by(WbQuestion.created_date.desc()).limit(limit).offset(offset)
        result = await self._session.execute(query)
        return list(result.scalars().all())

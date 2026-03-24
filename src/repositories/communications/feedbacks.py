"""Репозиторий: Отзывы покупателей."""
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.communications import WbFeedback


class FeedbacksRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def upsert_many(self, feedbacks: list[dict]) -> int:
        """Вставляет или обновляет отзывы. Возвращает кол-во обработанных записей."""
        if not feedbacks:
            return 0
        rows = [
            {
                "feedback_id": f.get("id", ""),
                "created_date": datetime.fromisoformat(f["createdDate"]) if f.get("createdDate") else None,
                "product_valuation": f.get("productValuation"),
                "was_viewed": f.get("wasViewed"),
                "text": f.get("text"),
                "nm_id": f.get("nmId"),
                "supplier_article": f.get("supplierArticle"),
                "subject_name": f.get("subjectName"),
                "answer_text": f.get("answer", {}).get("text") if f.get("answer") else None,
                "answer_state": f.get("answer", {}).get("state") if f.get("answer") else None,
                "user_name": f.get("userName"),
                "is_able_to_change_grade": f.get("isAbleToChangeGrade"),
                "photo": f.get("photoLinks"),
                "video": f.get("video"),
                "product_details": f.get("productDetails"),
                "fetched_at": datetime.utcnow(),
            }
            for f in feedbacks
        ]
        stmt = insert(WbFeedback).values(rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=["feedback_id"],
            set_={
                "created_date": stmt.excluded.created_date,
                "product_valuation": stmt.excluded.product_valuation,
                "was_viewed": stmt.excluded.was_viewed,
                "text": stmt.excluded.text,
                "nm_id": stmt.excluded.nm_id,
                "supplier_article": stmt.excluded.supplier_article,
                "subject_name": stmt.excluded.subject_name,
                "answer_text": stmt.excluded.answer_text,
                "answer_state": stmt.excluded.answer_state,
                "user_name": stmt.excluded.user_name,
                "is_able_to_change_grade": stmt.excluded.is_able_to_change_grade,
                "photo": stmt.excluded.photo,
                "video": stmt.excluded.video,
                "product_details": stmt.excluded.product_details,
                "fetched_at": stmt.excluded.fetched_at,
            },
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return len(rows)

    async def get_all(self, limit: int = 100, offset: int = 0) -> list[WbFeedback]:
        """Возвращает отзывы из БД (последние сначала)."""
        result = await self._session.execute(
            select(WbFeedback).order_by(WbFeedback.created_date.desc()).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def get_filtered(
        self,
        date_from: str | None = None,
        date_to: str | None = None,
        rating: int | None = None,
        is_answered: bool | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[WbFeedback]:
        """Возвращает отзывы с фильтрацией по параметрам."""
        query = select(WbFeedback)
        if date_from:
            query = query.where(WbFeedback.created_date >= datetime.fromisoformat(date_from))
        if date_to:
            query = query.where(WbFeedback.created_date <= datetime.fromisoformat(date_to))
        if rating is not None:
            query = query.where(WbFeedback.product_valuation == rating)
        if is_answered is not None:
            if is_answered:
                query = query.where(WbFeedback.answer_text.isnot(None))
            else:
                query = query.where(WbFeedback.answer_text.is_(None))
        query = query.order_by(WbFeedback.created_date.desc()).limit(limit).offset(offset)
        result = await self._session.execute(query)
        return list(result.scalars().all())

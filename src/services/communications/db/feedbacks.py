"""Сервис DB: Коммуникации — Чтение отзывов из БД."""
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.communications.feedbacks import FeedbacksRepository
from src.services.base import BaseService


class FeedbacksDbService(BaseService):

    async def get_feedbacks(
        self,
        session: AsyncSession,
        date_from: str | None = None,
        date_to: str | None = None,
        rating: int | None = None,
        is_answered: bool | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Возвращает отзывы из БД с фильтрацией."""
        repo = FeedbacksRepository(session)
        items = await repo.get_filtered(
            date_from=date_from,
            date_to=date_to,
            rating=rating,
            is_answered=is_answered,
            limit=limit,
            offset=offset,
        )
        return {
            "data": [
                {
                    "feedback_id": f.feedback_id,
                    "created_date": f.created_date.isoformat() if f.created_date else None,
                    "product_valuation": f.product_valuation,
                    "text": f.text,
                    "nm_id": f.nm_id,
                    "supplier_article": f.supplier_article,
                    "subject_name": f.subject_name,
                    "answer_text": f.answer_text,
                    "answer_state": f.answer_state,
                    "user_name": f.user_name,
                }
                for f in items
            ],
            "count": len(items),
        }

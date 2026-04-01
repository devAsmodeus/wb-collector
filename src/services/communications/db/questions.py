"""Сервис DB: Коммуникации — Чтение вопросов из БД."""
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.communications.questions import QuestionsRepository
from src.services.base import BaseService


class QuestionsDbService(BaseService):

    async def get_questions(
        self,
        session: AsyncSession,
        date_from: str | None = None,
        date_to: str | None = None,
        is_answered: bool | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Возвращает вопросы из БД с фильтрацией."""
        repo = QuestionsRepository(session)
        total = await repo.count()
        items = await repo.get_filtered(
            date_from=date_from,
            date_to=date_to,
            is_answered=is_answered,
            limit=limit,
            offset=offset,
        )
        return {
            "data": [
                {
                    "question_id": q.question_id,
                    "created_date": q.created_date.isoformat() if q.created_date else None,
                    "state": q.state,
                    "text": q.text,
                    "nm_id": q.nm_id,
                    "answer_text": q.answer_text,
                    "user_name": q.user_name,
                }
                for q in items
            ],
            "total": total,
            "limit": limit,
            "offset": offset,
        }

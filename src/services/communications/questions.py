"""Сервис: Коммуникации — Вопросы."""
from src.collectors.communications.questions import QuestionsCollector
from src.schemas.communications.questions import AnswerQuestionRequest
from src.services.base import BaseService


class QuestionsService(BaseService):
    async def get_count_unanswered(self) -> dict:
        async with QuestionsCollector() as c: return await c.get_count_unanswered()

    async def get_count(self, has_answer=None) -> dict:
        async with QuestionsCollector() as c: return await c.get_count(has_answer)

    async def get_list(self, is_answered=False, nm_id=None, limit=10, offset=0, order="dateDesc", date_from=None, date_to=None) -> dict:
        async with QuestionsCollector() as c:
            return await c.get_list(is_answered, nm_id, limit, offset, order, date_from, date_to)

    async def answer_question(self, data: AnswerQuestionRequest) -> dict:
        async with QuestionsCollector() as c: return await c.answer_question(data.model_dump(exclude_none=True))

    async def get_question(self, question_id: str) -> dict:
        async with QuestionsCollector() as c: return await c.get_question(question_id)

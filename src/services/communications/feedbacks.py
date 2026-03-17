"""Сервис: Коммуникации — Отзывы."""
from src.collectors.communications.feedbacks import FeedbacksCollector
from src.schemas.communications.feedbacks import AnswerFeedbackRequest, UpdateFeedbackAnswerRequest
from src.schemas.communications.chat import ReturnOrderRequest
from src.services.base import BaseService


class FeedbacksService(BaseService):
    async def get_count_unanswered(self) -> dict:
        async with FeedbacksCollector() as c: return await c.get_count_unanswered()

    async def get_count(self, has_answer=None) -> dict:
        async with FeedbacksCollector() as c: return await c.get_count(has_answer)

    async def get_list(self, is_answered=False, nm_id=None, limit=10, offset=0, order="dateDesc", date_from=None, date_to=None) -> dict:
        async with FeedbacksCollector() as c:
            return await c.get_list(is_answered, nm_id, limit, offset, order, date_from, date_to)

    async def answer_feedback(self, data: AnswerFeedbackRequest) -> dict:
        async with FeedbacksCollector() as c: return await c.answer_feedback(data.model_dump())

    async def update_feedback_answer(self, data: UpdateFeedbackAnswerRequest) -> dict:
        async with FeedbacksCollector() as c: return await c.update_feedback_answer(data.model_dump())

    async def request_return(self, data: ReturnOrderRequest) -> dict:
        async with FeedbacksCollector() as c: return await c.request_return(data.model_dump())

    async def get_feedback(self, feedback_id: str) -> dict:
        async with FeedbacksCollector() as c: return await c.get_feedback(feedback_id)

    async def get_archive(self, nm_id=None, limit=10, offset=0, order="dateDesc", date_from=None, date_to=None) -> dict:
        async with FeedbacksCollector() as c:
            return await c.get_archive(nm_id, limit, offset, order, date_from, date_to)

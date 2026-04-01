"""Сервис WB: Коммуникации — Новые вопросы/отзывы."""
from src.collectors.communications.new_items import NewItemsCollector
from src.services.base import BaseService


class NewItemsService(BaseService):
    async def get_new_feedbacks_questions(self) -> dict:
        async with NewItemsCollector() as c: return await c.get_new_feedbacks_questions()

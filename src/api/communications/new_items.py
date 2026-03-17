"""
Контроллер: Коммуникации / Новые вопросы и отзывы
WB API: feedbacks-api.wildberries.ru
Tag: (общая лента — 1 endpoint)
"""
from litestar import Controller, get

from src.services.communications.new_items import NewItemsService


class NewItemsController(Controller):
    path = "/"
    tags = ["Отзывы"]

    @get(
        "/new-feedbacks-questions",
        summary="Новые вопросы и отзывы",
        description=(
            "Возвращает количество новых необработанных отзывов и вопросов продавца.\n\n"
            "**WB endpoint:** `GET feedbacks-api.wildberries.ru/api/v1/new-feedbacks-questions`"
        ),
    )
    async def get_new_feedbacks_questions(self) -> dict:
        return await NewItemsService().get_new_feedbacks_questions()

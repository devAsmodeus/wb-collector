"""
Контроллер: Коммуникации / Отзывы
WB API: feedbacks-api.wildberries.ru
Tags: Отзывы (8 ep), Возвраты покупателями (2 ep)
"""
from litestar import Controller, get, patch, post
from litestar.params import Parameter

from src.schemas.communications.feedbacks import AnswerFeedbackRequest, UpdateFeedbackAnswerRequest
from src.schemas.communications.chat import ReturnOrderRequest
from src.services.communications.wb.feedbacks import FeedbacksService


class FeedbacksController(Controller):
    path = "/feedbacks"
    tags = ["09. API Wildberries"]

    @get(
        "/count-unanswered",
        summary="Количество необработанных отзывов",
        description=(
            "Возвращает количество новых отзывов, на которые продавец ещё не ответил.\n\n"
            "**WB endpoint:** `GET feedbacks-api.wildberries.ru/api/v1/feedbacks/count-unanswered`"
        ),
    )
    async def get_count_unanswered(self) -> dict:
        return await FeedbacksService().get_count_unanswered()

    @get(
        "/count",
        summary="Статистика по отзывам",
        description=(
            "Возвращает количество отвеченных, неотвеченных отзывов и отзывов в архиве.\n\n"
            "**WB endpoint:** `GET feedbacks-api.wildberries.ru/api/v1/feedbacks/count`"
        ),
    )
    async def get_count(
        self,
        has_answer: bool | None = Parameter(None, query="hasAnswer", description="`true` — отвеченные, `false` — неотвеченные."),
    ) -> dict:
        return await FeedbacksService().get_count(has_answer)

    @get(
        "/",
        summary="Список отзывов",
        description=(
            "Возвращает список отзывов с фильтрацией по статусу ответа, артикулу и дате.\n\n"
            "**WB endpoint:** `GET feedbacks-api.wildberries.ru/api/v1/feedbacks`"
        ),
    )
    async def get_list(
        self,
        is_answered: bool = Parameter(False, query="isAnswered", description="`true` — отвеченные, `false` — неотвеченные."),
        nm_id: int | None = Parameter(None, query="nmId", description="Фильтр по артикулу WB."),
        limit: int = Parameter(10, query="take", description="Количество в ответе. По умолчанию: 10."),
        offset: int = Parameter(0, query="skip", description="Смещение. По умолчанию: 0."),
        order: str = Parameter("dateDesc", query="order", description="Сортировка: `dateAsc`, `dateDesc`."),
        date_from: str | None = Parameter(None, query="dateFrom", description="Дата начала (ISO 8601)."),
        date_to: str | None = Parameter(None, query="dateTo", description="Дата окончания (ISO 8601)."),
    ) -> dict:
        return await FeedbacksService().get_list(is_answered, nm_id, limit, offset, order, date_from, date_to)

    @post(
        "/answer",
        summary="Ответить на отзыв",
        description=(
            "Добавляет ответ продавца на отзыв покупателя.\n\n"
            "**WB endpoint:** `POST feedbacks-api.wildberries.ru/api/v1/feedbacks/answer`"
        ),
    )
    async def answer_feedback(self, data: AnswerFeedbackRequest) -> dict:
        return await FeedbacksService().answer_feedback(data)

    @patch(
        "/answer",
        summary="Редактировать ответ на отзыв",
        description=(
            "Обновляет ответ продавца на отзыв.\n\n"
            "**WB endpoint:** `PATCH feedbacks-api.wildberries.ru/api/v1/feedbacks/answer`"
        ),
    )
    async def update_feedback_answer(self, data: UpdateFeedbackAnswerRequest) -> dict:
        return await FeedbacksService().update_feedback_answer(data)

    @post(
        "/return",
        tags=["09. API Wildberries"],
        summary="Запрос возврата по отзыву",
        description=(
            "Создаёт запрос на возврат товара покупателю на основании отзыва.\n\n"
            "**WB endpoint:** `POST feedbacks-api.wildberries.ru/api/v1/feedbacks/order/return`"
        ),
    )
    async def request_return(self, data: ReturnOrderRequest) -> dict:
        return await FeedbacksService().request_return(data)

    @get(
        "/{feedback_id:str}",
        summary="Один отзыв",
        description=(
            "Возвращает детальную информацию об отзыве по его ID.\n\n"
            "**WB endpoint:** `GET feedbacks-api.wildberries.ru/api/v1/feedback`"
        ),
    )
    async def get_feedback(
        self,
        feedback_id: str = Parameter(description="ID отзыва"),
    ) -> dict:
        return await FeedbacksService().get_feedback(feedback_id)

    @get(
        "/archive",
        tags=["09. API Wildberries"],
        summary="Архив отзывов",
        description=(
            "Возвращает архив отзывов с фильтрацией по артикулу и дате.\n\n"
            "**WB endpoint:** `GET feedbacks-api.wildberries.ru/api/v1/feedbacks/archive`"
        ),
    )
    async def get_archive(
        self,
        nm_id: int | None = Parameter(None, query="nmId", description="Фильтр по артикулу WB."),
        limit: int = Parameter(10, query="take", description="Количество в ответе. По умолчанию: 10."),
        offset: int = Parameter(0, query="skip", description="Смещение. По умолчанию: 0."),
        order: str = Parameter("dateDesc", query="order", description="Сортировка: `dateAsc`, `dateDesc`."),
        date_from: str | None = Parameter(None, query="dateFrom", description="Дата начала (ISO 8601)."),
        date_to: str | None = Parameter(None, query="dateTo", description="Дата окончания (ISO 8601)."),
    ) -> dict:
        return await FeedbacksService().get_archive(nm_id, limit, offset, order, date_from, date_to)

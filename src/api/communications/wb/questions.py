"""
Контроллер: Коммуникации / Вопросы
WB API: feedbacks-api.wildberries.ru
Tag: Вопросы (6 endpoints)
"""
from litestar import Controller, get, patch
from litestar.params import Parameter

from src.schemas.communications.questions import AnswerQuestionRequest
from src.services.communications.wb.questions import QuestionsService


class QuestionsController(Controller):
    path = "/questions"
    tags = ["Вопросы"]

    @get(
        "/count-unanswered",
        summary="Количество неотвеченных вопросов",
        description=(
            "Возвращает количество вопросов, на которые продавец ещё не ответил.\n\n"
            "**WB endpoint:** `GET feedbacks-api.wildberries.ru/api/v1/questions/count-unanswered`"
        ),
    )
    async def get_count_unanswered(self) -> dict:
        return await QuestionsService().get_count_unanswered()

    @get(
        "/count",
        summary="Статистика по вопросам",
        description=(
            "Возвращает количество отвеченных, неотвеченных вопросов и вопросов в архиве.\n\n"
            "**WB endpoint:** `GET feedbacks-api.wildberries.ru/api/v1/questions/count`"
        ),
    )
    async def get_count(
        self,
        has_answer: bool | None = Parameter(None, query="hasAnswer", description="`true` — отвеченные, `false` — неотвеченные."),
    ) -> dict:
        return await QuestionsService().get_count(has_answer)

    @get(
        "/",
        summary="Список вопросов",
        description=(
            "Возвращает список вопросов с фильтрацией по статусу ответа, артикулу и дате.\n\n"
            "**WB endpoint:** `GET feedbacks-api.wildberries.ru/api/v1/questions`"
        ),
    )
    async def get_list(
        self,
        is_answered: bool = Parameter(False, query="isAnswered", description="`true` — отвеченные, `false` — неотвеченные."),
        nm_id: int | None = Parameter(None, query="nmId", description="Фильтр по артикулу WB."),
        limit: int = Parameter(10, query="take", description="Количество вопросов в ответе. По умолчанию: 10."),
        offset: int = Parameter(0, query="skip", description="Смещение. По умолчанию: 0."),
        order: str = Parameter("dateDesc", query="order", description="Сортировка: `dateAsc`, `dateDesc`."),
        date_from: str | None = Parameter(None, query="dateFrom", description="Дата начала (ISO 8601)."),
        date_to: str | None = Parameter(None, query="dateTo", description="Дата окончания (ISO 8601)."),
    ) -> dict:
        return await QuestionsService().get_list(is_answered, nm_id, limit, offset, order, date_from, date_to)

    @patch(
        "/",
        summary="Ответить на вопрос / отклонить",
        description=(
            "Отвечает на вопрос покупателя или отклоняет его.\n\n"
            "**WB endpoint:** `PATCH feedbacks-api.wildberries.ru/api/v1/questions`"
        ),
    )
    async def answer_question(self, data: AnswerQuestionRequest) -> dict:
        return await QuestionsService().answer_question(data)

    @get(
        "/{question_id:str}",
        summary="Один вопрос",
        description=(
            "Возвращает детальную информацию об одном вопросе по его ID.\n\n"
            "**WB endpoint:** `GET feedbacks-api.wildberries.ru/api/v1/question`"
        ),
    )
    async def get_question(
        self,
        question_id: str = Parameter(description="ID вопроса"),
    ) -> dict:
        return await QuestionsService().get_question(question_id)

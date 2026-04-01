"""DB: Communications / Отзывы."""
from litestar import Controller, get
from litestar.params import Parameter
from src.services.communications.db.feedbacks import FeedbacksDbService
from src.utils.db_manager import DBManager


class DbFeedbacksController(Controller):
    path = "/feedbacks"
    tags = ["09. База данных"]

    @get(
        "/",
        summary="Отзывы из БД",
        description=(
            "Возвращает отзывы из таблицы `wb_feedbacks` с фильтрацией.\n\n"
            "Перед первым вызовом выполните `POST /communications/sync/feedbacks/full`."
        ),
    )
    async def get_feedbacks(
        self,
        date_from: str | None = Parameter(default=None, query="date_from", description="Дата начала (ISO 8601)"),
        date_to: str | None = Parameter(default=None, query="date_to", description="Дата окончания (ISO 8601)"),
        rating: int | None = Parameter(default=None, query="rating", description="Фильтр по оценке (1–5)"),
        is_answered: bool | None = Parameter(default=None, query="is_answered", description="Фильтр: отвечен / не отвечен"),
        limit: int = Parameter(default=100, query="limit", description="Кол-во записей (макс. 1000)"),
        offset: int = Parameter(default=0, query="offset", description="Смещение"),
    ) -> dict:
        async with DBManager() as db:
            return await FeedbacksDbService().get_feedbacks(
                db.session,
                date_from=date_from,
                date_to=date_to,
                rating=rating,
                is_answered=is_answered,
                limit=limit,
                offset=offset,
            )

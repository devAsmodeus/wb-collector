"""DB: Communications / Вопросы."""
from litestar import Controller, get
from litestar.params import Parameter
from src.services.communications.db.questions import QuestionsDbService
from src.utils.db_manager import DBManager


class DbQuestionsController(Controller):
    path = "/questions"
    tags = ["09. База данных"]

    @get(
        "/",
        summary="Вопросы из БД",
        description=(
            "Возвращает вопросы из таблицы `wb_questions` с фильтрацией.\n\n"
            "Перед первым вызовом выполните `POST /communications/sync/questions/full`."
        ),
    )
    async def get_questions(
        self,
        date_from: str | None = Parameter(default=None, query="date_from", description="Дата начала (ISO 8601)"),
        date_to: str | None = Parameter(default=None, query="date_to", description="Дата окончания (ISO 8601)"),
        is_answered: bool | None = Parameter(default=None, query="is_answered", description="Фильтр: отвечен / не отвечен"),
        limit: int = Parameter(default=100, query="limit", description="Кол-во записей (макс. 1000)"),
        offset: int = Parameter(default=0, query="offset", description="Смещение"),
    ) -> dict:
        async with DBManager() as db:
            return await QuestionsDbService().get_questions(
                db.session,
                date_from=date_from,
                date_to=date_to,
                is_answered=is_answered,
                limit=limit,
                offset=offset,
            )

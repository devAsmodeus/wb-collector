"""DB: Analytics / Поисковые запросы."""
from datetime import date

from litestar import Controller, get
from litestar.params import Parameter
from src.services.analytics.db.search import SearchDbService
from src.utils.db_manager import DBManager


class DbSearchController(Controller):
    path = "/search"
    tags = ["11. База данных"]

    @get(
        "/",
        summary="Поисковые запросы из БД",
        description=(
            "Возвращает поисковые запросы из таблицы `analytics_search_queries` с фильтрацией.\n\n"
            "Перед первым вызовом выполните `POST /analytics/sync/search/full`."
        ),
    )
    async def get_search_queries(
        self,
        nm_id: int | None = Parameter(default=None, query="nm_id", description="Фильтр по nm_id"),
        text: str | None = Parameter(default=None, query="text", description="Поиск по тексту запроса (ilike)"),
        date_from: date | None = Parameter(default=None, query="date_from", description="Дата начала (YYYY-MM-DD)"),
        date_to: date | None = Parameter(default=None, query="date_to", description="Дата окончания (YYYY-MM-DD)"),
        limit: int = Parameter(default=100, query="limit", description="Кол-во записей (макс. 1000)"),
        offset: int = Parameter(default=0, query="offset", description="Смещение"),
    ) -> dict:
        async with DBManager() as db:
            return await SearchDbService().get_search_queries(
                db.session,
                nm_id=nm_id,
                text=text,
                date_from=date_from,
                date_to=date_to,
                limit=limit,
                offset=offset,
            )

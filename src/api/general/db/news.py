"""DB: General / Новости."""
from litestar import Controller, get
from litestar.params import Parameter
from src.services.general.db.news import NewsDbService
from src.utils.db_manager import DBManager


class DbNewsController(Controller):
    path = "/news"
    tags = ["DB / General"]

    @get(
        "/",
        summary="Новости из БД",
        description=(
            "Возвращает новости из таблицы `wb_news` (последние сначала).\n\n"
            "Перед первым вызовом выполните `POST /general/sync/news/full`."
        ),
    )
    async def get_news(
        self,
        limit: int = Parameter(default=100, query="limit", description="Кол-во записей (макс. 1000)"),
        offset: int = Parameter(default=0, query="offset", description="Смещение"),
    ) -> dict:
        async with DBManager() as db:
            return await NewsDbService().get_from_db(db.session, limit=limit, offset=offset)

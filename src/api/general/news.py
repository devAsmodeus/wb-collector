"""
Контроллер: General / Новости
WB API: common-api.wildberries.ru
"""
from litestar import Controller, get, post
from litestar.params import Parameter

from src.schemas.general.news import NewsResponse
from src.services.general.news import NewsService
from src.utils.db_manager import DBManager


class NewsController(Controller):
    path = "/news"
    tags = ["General — Новости"]

    @get(
        "/",
        summary="Новости портала продавцов (WB API)",
        description=(
            "Проксирует запрос к WB API. Данные не сохраняются в БД.\n\n"
            "По умолчанию (без параметров) отдаёт новости за последние **90 дней**.\n\n"
            "**WB endpoint:** `GET common-api.wildberries.ru/api/communications/v2/news`"
        ),
    )
    async def get_news(
        self,
        from_date: str | None = Parameter(
            None,
            query="from_date",
            description="Дата начала выборки ISO 8601 (напр. `2024-01-01`).",
        ),
        from_id: int | None = Parameter(
            None,
            query="from_id",
            description="ID новости, начиная с которой вернуть список.",
        ),
    ) -> NewsResponse:
        return await NewsService().get_news(from_date=from_date, from_id=from_id)

    @post(
        "/sync/full",
        summary="Полная синхронизация новостей в БД",
        description=(
            "Загружает все новости с 2020-01-01 и сохраняет в таблицу `wb_news`.\n\n"
            "Используйте один раз для начального заполнения. "
            "Для ежедневного обновления используйте `/news/sync/incremental`.\n\n"
            "**WB endpoint:** `GET common-api.wildberries.ru/api/communications/v2/news`"
        ),
    )
    async def sync_news_full(self) -> dict:
        async with DBManager() as db:
            return await NewsService().sync_all(db.session)

    @post(
        "/sync/incremental",
        summary="Инкрементальная синхронизация новостей",
        description=(
            "Загружает только новые новости (начиная с последнего сохранённого ID).\n\n"
            "Если БД пуста — автоматически делает полную выгрузку.\n\n"
            "**WB endpoint:** `GET common-api.wildberries.ru/api/communications/v2/news`"
        ),
    )
    async def sync_news_incremental(self) -> dict:
        async with DBManager() as db:
            return await NewsService().sync_incremental(db.session)

    @get(
        "/db",
        summary="Новости из БД",
        description=(
            "Возвращает новости, сохранённые в таблице `wb_news`.\n\n"
            "Перед первым вызовом выполните `POST /general/news/sync/full`."
        ),
    )
    async def get_news_from_db(
        self,
        limit: int = Parameter(100, query="limit", description="Кол-во записей (макс. 1000)"),
        offset: int = Parameter(0, query="offset", description="Смещение"),
    ) -> dict:
        async with DBManager() as db:
            return await NewsService().get_from_db(db.session, limit=limit, offset=offset)

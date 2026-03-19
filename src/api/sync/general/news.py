"""Sync: General / Новости."""
from litestar import Controller, post
from src.services.general.news import NewsService
from src.utils.db_manager import DBManager


class SyncNewsController(Controller):
    path = "/news"
    tags = ["Sync / General"]

    @post(
        "/full",
        summary="Полная выгрузка новостей в БД",
        description=(
            "Загружает все новости с 2020-01-01 и сохраняет в `wb_news`.\n\n"
            "Используйте один раз для начального заполнения.\n\n"
            "**WB:** `GET common-api.wildberries.ru/api/communications/v2/news`"
        ),
    )
    async def sync_news_full(self) -> dict:
        async with DBManager() as db:
            return await NewsService().sync_all(db.session)

    @post(
        "/incremental",
        summary="Инкрементальная синхронизация новостей",
        description=(
            "Загружает только новые новости (начиная с последнего `news_id` в БД).\n\n"
            "Если БД пуста — автоматически делает полную выгрузку.\n\n"
            "**WB:** `GET common-api.wildberries.ru/api/communications/v2/news`"
        ),
    )
    async def sync_news_incremental(self) -> dict:
        async with DBManager() as db:
            return await NewsService().sync_incremental(db.session)

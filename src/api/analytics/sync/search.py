"""Sync: Analytics / Поисковые запросы."""
from litestar import Controller, post
from src.services.analytics.sync.search import SearchSyncService
from src.utils.db_manager import DBManager


class SyncSearchController(Controller):
    path = "/search"
    tags = ["11. Синхронизация"]

    @post(
        "/full",
        summary="Полная выгрузка поисковых запросов в БД",
        description=(
            "Загружает поисковые запросы за последние 7 дней "
            "и сохраняет в `analytics_search_queries`.\n\n"
            "**WB:** `POST seller-analytics-api.wildberries.ru/api/v2/search-report/report`\n\n"
            "**Ограничение:** skip + take <= 10000."
        ),
    )
    async def sync_search_full(self) -> dict:
        async with DBManager() as db:
            return await SearchSyncService().sync_search_full(db.session)

    @post(
        "/incremental",
        summary="Инкрементальная выгрузка поисковых запросов в БД",
        description=(
            "Загружает поисковые запросы с max(period_start) из БД по сегодня.\n\n"
            "Если БД пуста — выполняет полную синхронизацию.\n\n"
            "**WB:** `POST seller-analytics-api.wildberries.ru/api/v2/search-report/report`"
        ),
    )
    async def sync_search_incremental(self) -> dict:
        async with DBManager() as db:
            return await SearchSyncService().sync_search_incremental(db.session)

"""Sync: Analytics / Остатки по группам."""
from litestar import Controller, post
from src.services.analytics.sync.stocks import StocksSyncService
from src.utils.db_manager import DBManager


class SyncStocksController(Controller):
    path = "/stocks"
    tags = ["11. Синхронизация"]

    @post(
        "/full",
        summary="Полная выгрузка остатков по группам в БД",
        description=(
            "Загружает аналитику остатков за последние 30 дней "
            "и сохраняет в `analytics_stocks_groups`.\n\n"
            "**WB:** `POST seller-analytics-api.wildberries.ru/api/v2/stocks-report/products/groups`"
        ),
    )
    async def sync_stocks_full(self) -> dict:
        async with DBManager() as db:
            return await StocksSyncService().sync_stocks_full(db.session)

    @post(
        "/incremental",
        summary="Инкрементальная выгрузка остатков по группам в БД",
        description=(
            "Загружает остатки с max(period_start) из БД по сегодня.\n\n"
            "Если БД пуста — выполняет полную синхронизацию.\n\n"
            "**WB:** `POST seller-analytics-api.wildberries.ru/api/v2/stocks-report/products/groups`"
        ),
    )
    async def sync_stocks_incremental(self) -> dict:
        async with DBManager() as db:
            return await StocksSyncService().sync_stocks_incremental(db.session)

"""Sync: Analytics / Воронка продаж."""
from litestar import Controller, post
from src.services.analytics.sync.funnel import FunnelSyncService
from src.utils.db_manager import DBManager


class SyncFunnelController(Controller):
    path = "/funnel"
    tags = ["11. Синхронизация"]

    @post(
        "/full",
        summary="Полная выгрузка воронки продаж в БД",
        description=(
            "Загружает воронку продаж за последние 30 дней для всех nm_id из `wb_cards` "
            "и сохраняет в `analytics_funnel_products`.\n\n"
            "**WB:** `POST seller-analytics-api.wildberries.ru/api/analytics/v3/sales-funnel/products`\n\n"
            "**Предварительно:** выполните `POST /products/sync/cards/full` для заполнения `wb_cards`."
        ),
    )
    async def sync_funnel_full(self) -> dict:
        async with DBManager() as db:
            return await FunnelSyncService().sync_funnel_full(db.session)

    @post(
        "/incremental",
        summary="Инкрементальная выгрузка воронки продаж в БД",
        description=(
            "Загружает воронку продаж с max(date) из БД по сегодня.\n\n"
            "Если БД пуста — выполняет полную синхронизацию.\n\n"
            "**WB:** `POST seller-analytics-api.wildberries.ru/api/analytics/v3/sales-funnel/products`"
        ),
    )
    async def sync_funnel_incremental(self) -> dict:
        async with DBManager() as db:
            return await FunnelSyncService().sync_funnel_incremental(db.session)

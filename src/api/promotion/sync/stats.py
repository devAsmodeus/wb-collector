"""Sync: Маркетинг / Статистика кампаний."""
from litestar import Controller, post
from src.services.promotion.sync.stats import StatsSyncService
from src.utils.db_manager import DBManager


class SyncStatsController(Controller):
    path = "/stats"
    tags = ["Sync / Promotion"]

    @post(
        "/full",
        summary="Полная выгрузка статистики кампаний в БД",
        description=(
            "Загружает статистику по всем кампаниям и сохраняет в `wb_campaign_stats`.\n\n"
            "**WB:** `GET advert-api.wildberries.ru/adv/v3/fullstats`"
        ),
    )
    async def sync_stats_full(self) -> dict:
        async with DBManager() as db:
            return await StatsSyncService().sync_stats(db.session)

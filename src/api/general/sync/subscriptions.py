"""Sync: Общее — Подписки Джем."""
from litestar import Controller, post

from src.schemas.general.subscriptions import SubscriptionsJamInfo
from src.services.general.sync.subscriptions import SubscriptionsSyncService
from src.utils.db_manager import DBManager


class SyncSubscriptionsController(Controller):
    path = "/subscriptions"
    tags = ["01. Синхронизация"]

    @post("/full", summary="Полная синхронизация подписок Джем WB → БД")
    async def sync_subscriptions_full(self) -> SubscriptionsJamInfo:
        async with DBManager() as db:
            return await SubscriptionsSyncService().sync_full(db.session)

    @post("/incremental", summary="Инкрементальная синхронизация подписок Джем WB → БД")
    async def sync_subscriptions_incremental(self) -> SubscriptionsJamInfo:
        # Подписка — одна запись, incremental идентичен full
        async with DBManager() as db:
            return await SubscriptionsSyncService().sync_full(db.session)

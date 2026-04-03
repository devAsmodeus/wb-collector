"""Sync: General / Подписки Джем."""
from litestar import Controller, post
from src.schemas.general.subscriptions import SubscriptionsJamInfo
from src.services.general.sync.subscriptions import SubscriptionsSyncService
from src.utils.db_manager import DBManager


class SyncSubscriptionsController(Controller):
    path = "/subscriptions"
    tags = ["01. Синхронизация"]

    @post(
        "/full",
        summary="Синхронизировать подписки Джем",
        description=(
            "Запрашивает подписки у WB и сохраняет/обновляет запись в таблице `wb_seller_subscriptions`.\n\n"
            "**WB:** `GET common-api.wildberries.ru/api/common/v1/subscriptions`"
        ),
    )
    async def sync_subscriptions_full(self) -> SubscriptionsJamInfo:
        async with DBManager() as db:
            return await SubscriptionsSyncService().sync_full(db.session)

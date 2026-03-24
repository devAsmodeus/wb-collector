"""Sync: FBS / Сборочные задания."""
from litestar import Controller, post
from src.services.fbs.sync.orders import FbsOrdersSyncService
from src.utils.db_manager import DBManager


class SyncFbsOrdersController(Controller):
    path = "/orders"
    tags = ["Sync / FBS"]

    @post(
        "/full",
        summary="Полная синхронизация заказов FBS в БД",
        description=(
            "Загружает все сборочные задания FBS из WB API и сохраняет в `fbs_orders`.\n\n"
            "**WB:** `GET marketplace-api.wildberries.ru/api/v3/orders`"
        ),
    )
    async def sync_orders_full(self) -> dict:
        async with DBManager() as db:
            return await FbsOrdersSyncService().sync_orders(db.session)

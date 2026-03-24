"""Sync: DBW / Сборочные задания."""
from litestar import Controller, post
from src.services.dbw.sync.orders import DBWOrdersSyncService
from src.utils.db_manager import DBManager


class SyncDBWOrdersController(Controller):
    path = "/orders"
    tags = ["Sync / DBW"]

    @post(
        "/full",
        summary="Полная синхронизация заказов DBW в БД",
        description=(
            "Загружает все заказы DBW из WB API и сохраняет/обновляет в таблице `dbw_orders`.\n\n"
            "**WB:** `GET marketplace-api.wildberries.ru/api/v3/dbw/orders`"
        ),
    )
    async def sync_orders_full(self) -> dict:
        async with DBManager() as db:
            return await DBWOrdersSyncService().sync_orders(db.session)

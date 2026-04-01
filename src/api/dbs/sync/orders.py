"""Sync: DBS / Сборочные задания."""
from litestar import Controller, post
from src.services.dbs.sync.orders import DBSOrdersSyncService
from src.utils.db_manager import DBManager


class SyncDBSOrdersController(Controller):
    path = "/orders"
    tags = ["05. Синхронизация"]

    @post(
        "/full",
        summary="Полная синхронизация заказов DBS в БД",
        description=(
            "Загружает все заказы DBS из WB API и сохраняет/обновляет в таблице `dbs_orders`.\n\n"
            "**WB:** `GET marketplace-api.wildberries.ru/api/v3/dbs/orders`"
        ),
    )
    async def sync_orders_full(self) -> dict:
        async with DBManager() as db:
            return await DBSOrdersSyncService().sync_orders(db.session)

    @post(
        "/incremental",
        summary="Инкрементальная синхронизация заказов DBS",
        description=(
            "Загружает только новые заказы DBS (начиная с последней даты в БД).\n\n"
            "Если БД пуста — автоматически делает полную выгрузку.\n\n"
            "**WB:** `GET marketplace-api.wildberries.ru/api/v3/dbs/orders`"
        ),
    )
    async def sync_orders_incremental(self) -> dict:
        async with DBManager() as db:
            return await DBSOrdersSyncService().sync_incremental(db.session)

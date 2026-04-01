"""Sync: Самовывоз / Сборочные задания."""
from litestar import Controller, post
from src.services.pickup.sync.orders import PickupOrdersSyncService
from src.utils.db_manager import DBManager


class SyncPickupOrdersController(Controller):
    path = "/orders"
    tags = ["06. Синхронизация"]

    @post(
        "/full",
        summary="Полная синхронизация заказов Самовывоз в БД",
        description=(
            "Загружает все заказы Самовывоз из WB API и сохраняет/обновляет в таблице `pickup_orders`.\n\n"
            "**WB:** `GET marketplace-api.wildberries.ru/api/v3/click-collect/orders`"
        ),
    )
    async def sync_orders_full(self) -> dict:
        async with DBManager() as db:
            return await PickupOrdersSyncService().sync_orders(db.session)

    @post(
        "/incremental",
        summary="Инкрементальная синхронизация заказов Самовывоз",
        description=(
            "Загружает только новые заказы Самовывоз (начиная с последней даты в БД).\n\n"
            "Если БД пуста — автоматически делает полную выгрузку.\n\n"
            "**WB:** `GET marketplace-api.wildberries.ru/api/v3/click-collect/orders`"
        ),
    )
    async def sync_orders_incremental(self) -> dict:
        async with DBManager() as db:
            return await PickupOrdersSyncService().sync_incremental(db.session)

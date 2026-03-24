"""Sync: Products / Склады продавца."""
from litestar import Controller, post
from src.services.products.sync.warehouses import WarehousesSyncService
from src.utils.db_manager import DBManager


class SyncWarehousesController(Controller):
    path = "/warehouses"
    tags = ["Sync / Products"]

    @post(
        "/full",
        summary="Полная выгрузка складов продавца в БД",
        description=(
            "Загружает склады продавца и сохраняет в `wb_warehouses`.\n\n"
            "**WB:** `GET marketplace-api.wildberries.ru/api/v3/warehouses`"
        ),
    )
    async def sync_warehouses_full(self) -> dict:
        async with DBManager() as db:
            return await WarehousesSyncService().sync_warehouses(db.session)

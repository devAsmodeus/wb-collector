"""Sync: Products / Склады продавца."""
from litestar import Controller, post
from src.services.products.sync.warehouses import WarehousesSyncService
from src.utils.db_manager import DBManager


class SyncWarehousesController(Controller):
    path = "/warehouses"
    tags = ["02. Синхронизация"]

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

    @post(
        "/incremental",
        summary="Инкрементальная выгрузка складов продавца в БД",
        description=(
            "Склады — справочные данные, инкрементальная = полная синхронизация.\n\n"
            "**WB:** `GET marketplace-api.wildberries.ru/api/v3/warehouses`"
        ),
    )
    async def sync_warehouses_incremental(self) -> dict:
        async with DBManager() as db:
            return await WarehousesSyncService().sync_warehouses_incremental(db.session)

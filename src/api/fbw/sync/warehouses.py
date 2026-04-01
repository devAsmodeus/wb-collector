"""Sync: FBW / Склады WB для FBW-поставок."""
from litestar import Controller, post
from src.services.fbw.sync.warehouses import FbwWarehousesSyncService
from src.utils.db_manager import DBManager


class SyncFbwWarehousesController(Controller):
    path = "/warehouses"
    tags = ["07. Синхронизация"]

    @post(
        "/full",
        summary="Полная выгрузка складов WB для FBW в БД",
        description=(
            "Загружает список складов WB, принимающих FBW-поставки, и сохраняет в `fbw_warehouses`.\n\n"
            "**WB:** `GET marketplace-api.wildberries.ru/api/v1/warehouses`"
        ),
    )
    async def sync_warehouses_full(self) -> dict:
        async with DBManager() as db:
            return await FbwWarehousesSyncService().sync_warehouses_full(db.session)

    @post(
        "/incremental",
        summary="Инкрементальная выгрузка складов WB для FBW в БД",
        description=(
            "Склады — справочные данные, инкрементальная синхронизация = полная.\n\n"
            "**WB:** `GET marketplace-api.wildberries.ru/api/v1/warehouses`"
        ),
    )
    async def sync_warehouses_incremental(self) -> dict:
        async with DBManager() as db:
            return await FbwWarehousesSyncService().sync_warehouses_incremental(db.session)

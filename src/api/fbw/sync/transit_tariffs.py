"""Sync: FBW / Тарифы транзитной доставки."""
from litestar import Controller, post
from src.services.fbw.sync.transit_tariffs import FbwTransitTariffsSyncService
from src.utils.db_manager import DBManager


class SyncFbwTransitTariffsController(Controller):
    path = "/transit-tariffs"
    tags = ["07. Синхронизация"]

    @post(
        "/full",
        summary="Полная выгрузка тарифов транзита FBW в БД",
        description=(
            "Загружает тарифы транзитной доставки между складами WB и сохраняет в `fbw_transit_tariffs`.\n\n"
            "**WB:** `GET marketplace-api.wildberries.ru/api/v1/transit-tariffs`"
        ),
    )
    async def sync_transit_tariffs_full(self) -> dict:
        async with DBManager() as db:
            return await FbwTransitTariffsSyncService().sync_transit_tariffs_full(db.session)

    @post(
        "/incremental",
        summary="Инкрементальная выгрузка тарифов транзита FBW в БД",
        description=(
            "Тарифы — справочные данные, инкрементальная синхронизация = полная.\n\n"
            "**WB:** `GET marketplace-api.wildberries.ru/api/v1/transit-tariffs`"
        ),
    )
    async def sync_transit_tariffs_incremental(self) -> dict:
        async with DBManager() as db:
            return await FbwTransitTariffsSyncService().sync_transit_tariffs_incremental(db.session)

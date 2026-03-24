"""Sync: Tariffs — Синхронизация тарифов WB в БД."""
from litestar import Controller, post
from src.services.tariffs.sync.tariffs import TariffsSyncService
from src.utils.db_manager import DBManager


class SyncCommissionsController(Controller):
    path = "/commissions"
    tags = ["Sync / Tariffs"]

    @post(
        "/",
        summary="Синхронизация комиссий по категориям",
        description=(
            "Загружает комиссии WB по категориям товаров и сохраняет в `wb_tariffs_commission`.\n\n"
            "**WB:** `GET common-api.wildberries.ru/api/v1/tariffs/commission`"
        ),
    )
    async def sync_commissions(self) -> dict:
        async with DBManager() as db:
            return await TariffsSyncService().sync_commissions(db.session)


class SyncBoxController(Controller):
    path = "/box"
    tags = ["Sync / Tariffs"]

    @post(
        "/",
        summary="Синхронизация тарифов коробами",
        description=(
            "Загружает тарифы на доставку и хранение коробами и сохраняет в `wb_tariffs_box`.\n\n"
            "**WB:** `GET common-api.wildberries.ru/api/v1/tariffs/box`"
        ),
    )
    async def sync_box_tariffs(self) -> dict:
        async with DBManager() as db:
            return await TariffsSyncService().sync_box_tariffs(db.session)


class SyncPalletController(Controller):
    path = "/pallet"
    tags = ["Sync / Tariffs"]

    @post(
        "/",
        summary="Синхронизация тарифов паллетами",
        description=(
            "Загружает тарифы на доставку и хранение паллетами и сохраняет в `wb_tariffs_pallet`.\n\n"
            "**WB:** `GET common-api.wildberries.ru/api/v1/tariffs/pallet`"
        ),
    )
    async def sync_pallet_tariffs(self) -> dict:
        async with DBManager() as db:
            return await TariffsSyncService().sync_pallet_tariffs(db.session)


class SyncSupplyController(Controller):
    path = "/supply"
    tags = ["Sync / Tariffs"]

    @post(
        "/",
        summary="Синхронизация коэффициентов поставок",
        description=(
            "Загружает коэффициенты складов для поставок и сохраняет в `wb_tariffs_supply`.\n\n"
            "**WB:** `GET common-api.wildberries.ru/api/v1/tariffs/warehouseCoeff`"
        ),
    )
    async def sync_supply_tariffs(self) -> dict:
        async with DBManager() as db:
            return await TariffsSyncService().sync_supply_tariffs(db.session)

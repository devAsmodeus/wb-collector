"""Sync: Tariffs — Синхронизация тарифов WB в БД."""
from litestar import Controller, post
from src.services.tariffs.sync.tariffs import TariffsSyncService
from src.utils.db_manager import DBManager


class SyncCommissionsController(Controller):
    path = "/commissions"
    tags = ["10. Синхронизация"]

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

    @post(
        "/incremental",
        summary="Инкрементальная синхронизация комиссий",
        description=(
            "Комиссии — справочные данные, инкрементальная = полная синхронизация (upsert обновит данные).\n\n"
            "**WB:** `GET common-api.wildberries.ru/api/v1/tariffs/commission`"
        ),
    )
    async def sync_commissions_incremental(self) -> dict:
        async with DBManager() as db:
            result = await TariffsSyncService().sync_commissions(db.session)
            result["source"] = "incremental"
            return result


class SyncBoxController(Controller):
    path = "/box"
    tags = ["10. Синхронизация"]

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

    @post(
        "/incremental",
        summary="Инкрементальная синхронизация тарифов коробами",
        description=(
            "Тарифы коробами — справочные данные, инкрементальная = полная синхронизация.\n\n"
            "**WB:** `GET common-api.wildberries.ru/api/v1/tariffs/box`"
        ),
    )
    async def sync_box_tariffs_incremental(self) -> dict:
        async with DBManager() as db:
            result = await TariffsSyncService().sync_box_tariffs(db.session)
            result["source"] = "incremental"
            return result


class SyncPalletController(Controller):
    path = "/pallet"
    tags = ["10. Синхронизация"]

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

    @post(
        "/incremental",
        summary="Инкрементальная синхронизация тарифов паллетами",
        description=(
            "Тарифы паллетами — справочные данные, инкрементальная = полная синхронизация.\n\n"
            "**WB:** `GET common-api.wildberries.ru/api/v1/tariffs/pallet`"
        ),
    )
    async def sync_pallet_tariffs_incremental(self) -> dict:
        async with DBManager() as db:
            result = await TariffsSyncService().sync_pallet_tariffs(db.session)
            result["source"] = "incremental"
            return result


class SyncSupplyController(Controller):
    path = "/supply"
    tags = ["10. Синхронизация"]

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

    @post(
        "/incremental",
        summary="Инкрементальная синхронизация коэффициентов поставок",
        description=(
            "Коэффициенты поставок — справочные данные, инкрементальная = полная синхронизация.\n\n"
            "**WB:** `GET common-api.wildberries.ru/api/v1/tariffs/warehouseCoeff`"
        ),
    )
    async def sync_supply_tariffs_incremental(self) -> dict:
        async with DBManager() as db:
            result = await TariffsSyncService().sync_supply_tariffs(db.session)
            result["source"] = "incremental"
            return result

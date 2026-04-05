"""Sync: FBS / Поставки."""
from litestar import Controller, post
from src.services.fbs.sync.supplies import FbsSuppliesSyncService
from src.utils.db_manager import DBManager


class SyncFbsSuppliesController(Controller):
    path = "/supplies"
    tags = ["03. Синхронизация"]

    @post(
        "/full",
        summary="Полная синхронизация поставок FBS в БД",
        description=(
            "Загружает все поставки FBS из WB API и сохраняет в `fbs_supplies`.\n\n"
            "**WB:** `GET marketplace-api.wildberries.ru/api/v3/supplies`"
        ),
    )
    async def sync_supplies_full(self) -> dict:
        async with DBManager() as db:
            return await FbsSuppliesSyncService().sync_supplies(db.session)

    @post(
        "/incremental",
        summary="Инкрементальная синхронизация поставок FBS",
        description=(
            "Загружает поставки FBS (те же данные, обновляет существующие).\n\n"
            "**WB:** `GET marketplace-api.wildberries.ru/api/v3/supplies`"
        ),
    )
    async def sync_supplies_incremental(self) -> dict:
        async with DBManager() as db:
            return await FbsSuppliesSyncService().sync_supplies(db.session)

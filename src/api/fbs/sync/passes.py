"""Sync: FBS / Пропуска."""
from litestar import Controller, post
from src.services.fbs.sync.passes import FbsPassesSyncService
from src.utils.db_manager import DBManager


class SyncFbsPassesController(Controller):
    path = "/passes"
    tags = ["03. Синхронизация"]

    @post(
        "/full",
        summary="Полная синхронизация пропусков FBS в БД",
        description=(
            "Загружает все пропуска на склад WB и сохраняет в `fbs_passes`.\n\n"
            "**WB:** `GET marketplace-api.wildberries.ru/api/v3/passes`"
        ),
    )
    async def sync_passes_full(self) -> dict:
        async with DBManager() as db:
            return await FbsPassesSyncService().sync_passes(db.session)

    @post(
        "/incremental",
        summary="Инкрементальная синхронизация пропусков FBS",
        description=(
            "Загружает пропуска (те же данные, обновляет существующие).\n\n"
            "**WB:** `GET marketplace-api.wildberries.ru/api/v3/passes`"
        ),
    )
    async def sync_passes_incremental(self) -> dict:
        async with DBManager() as db:
            return await FbsPassesSyncService().sync_passes(db.session)

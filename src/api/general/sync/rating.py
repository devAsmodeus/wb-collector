"""Sync: Общее — Рейтинг продавца."""
from litestar import Controller, post

from src.schemas.general.rating import SupplierRatingModel
from src.services.general.sync.rating import RatingSyncService
from src.utils.db_manager import DBManager


class SyncRatingController(Controller):
    path = "/rating"
    tags = ["01. Синхронизация"]

    @post("/full", summary="Полная синхронизация рейтинга продавца WB → БД")
    async def sync_rating_full(self) -> SupplierRatingModel:
        async with DBManager() as db:
            return await RatingSyncService().sync_full(db.session)

    @post("/incremental", summary="Инкрементальная синхронизация рейтинга продавца WB → БД")
    async def sync_rating_incremental(self) -> SupplierRatingModel:
        # Рейтинг — одна запись, incremental идентичен full
        async with DBManager() as db:
            return await RatingSyncService().sync_full(db.session)

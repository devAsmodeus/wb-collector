"""Sync: Общее — Продавец."""
from litestar import Controller, post

from src.schemas.general.seller import SellerInfo
from src.services.general.sync.seller import SellerSyncService
from src.utils.db_manager import DBManager


class SyncSellerController(Controller):
    path = "/seller"
    tags = ["01. Синхронизация"]

    @post("/full", summary="Полная синхронизация информации о продавце WB → БД")
    async def sync_seller_full(self) -> SellerInfo:
        return await SellerSyncService(db=DBManager()).sync_seller_info()

    @post("/incremental", summary="Инкрементальная синхронизация информации о продавце WB → БД")
    async def sync_seller_incremental(self) -> SellerInfo:
        # Данные продавца — одна запись, incremental идентичен full
        return await SellerSyncService(db=DBManager()).sync_seller_info()

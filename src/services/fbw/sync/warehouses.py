"""Сервис Sync: FBW — Синхронизация складов WB для FBW-поставок."""
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.fbw.acceptance import FBWAcceptanceCollector
from src.repositories.fbw.warehouses import FbwWarehousesRepository
from src.services.base import BaseService

logger = logging.getLogger(__name__)


class FbwWarehousesSyncService(BaseService):

    async def sync_warehouses_full(self, session: AsyncSession) -> dict:
        """Полная выгрузка складов WB для FBW-поставок."""
        repo = FbwWarehousesRepository(session)

        async with FBWAcceptanceCollector() as collector:
            response = await collector.get_warehouses()

        warehouses = response.warehouses or []
        items = [
            {
                "id": wh.id,
                "name": wh.name,
                "address": wh.address,
                "work_time": wh.workTime,
                "accepts_qr": wh.acceptsQR,
                "raw_data": wh.model_dump(),
            }
            for wh in warehouses
            if wh.id is not None
        ]

        saved = await repo.upsert_many(items)
        logger.info(f"FBW warehouses synced: {saved} warehouses saved")
        return {"synced": saved, "source": "full"}

    async def sync_warehouses_incremental(self, session: AsyncSession) -> dict:
        """
        Инкрементальная синхронизация складов FBW.
        Склады — справочные данные, incremental = full sync.
        """
        result = await self.sync_warehouses_full(session)
        result["source"] = "incremental"
        return result

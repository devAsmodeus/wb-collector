"""Сервис Sync: Товары — Синхронизация складов продавца."""
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.products import ProductsCollector
from src.repositories.products.warehouses import WarehousesRepository
from src.services.base import BaseService

logger = logging.getLogger(__name__)


class WarehousesSyncService(BaseService):

    async def sync_warehouses(self, session: AsyncSession) -> dict:
        """Полная выгрузка складов продавца."""
        repo = WarehousesRepository(session)

        async with ProductsCollector() as collector:
            response = await collector.warehouses.get_seller_warehouses()

        warehouses = response.result if response.result else []
        saved = await repo.upsert_many(warehouses)
        logger.info(f"Warehouses synced: {saved} warehouses saved")
        return {"synced": saved, "source": "full"}

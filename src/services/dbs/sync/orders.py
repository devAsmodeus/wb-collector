"""Сервис Sync: DBS — Синхронизация заказов."""
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.dbs.orders import DBSOrdersCollector
from src.repositories.dbs.orders import DbsOrdersRepository
from src.services.base import BaseService

logger = logging.getLogger(__name__)


class DBSOrdersSyncService(BaseService):

    async def sync_orders(self, session: AsyncSession) -> dict:
        """
        Полная выгрузка заказов DBS из WB API и сохранение в БД.
        """
        repo = DbsOrdersRepository(session)

        async with DBSOrdersCollector() as collector:
            response = await collector.get_orders()

        orders_data = [
            o.model_dump() if hasattr(o, "model_dump") else o
            for o in (response.orders or [])
        ]

        saved = await repo.upsert_many(orders_data)
        logger.info(f"DBS orders synced: {saved} orders saved")
        return {"synced": saved, "source": "full"}

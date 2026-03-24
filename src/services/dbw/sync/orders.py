"""Сервис Sync: DBW — Синхронизация заказов."""
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.dbw.orders import DBWOrdersCollector
from src.repositories.dbw.orders import DbwOrdersRepository
from src.services.base import BaseService

logger = logging.getLogger(__name__)


class DBWOrdersSyncService(BaseService):

    async def sync_orders(self, session: AsyncSession) -> dict:
        """
        Полная выгрузка заказов DBW из WB API и сохранение в БД.
        """
        repo = DbwOrdersRepository(session)

        async with DBWOrdersCollector() as collector:
            response = await collector.get_orders()

        orders_data = [
            o.model_dump() if hasattr(o, "model_dump") else o
            for o in (response.orders or [])
        ]

        saved = await repo.upsert_many(orders_data)
        logger.info(f"DBW orders synced: {saved} orders saved")
        return {"synced": saved, "source": "full"}

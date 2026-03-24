"""Сервис Sync: Самовывоз — Синхронизация заказов."""
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.pickup.orders import PickupOrdersCollector
from src.repositories.pickup.orders import PickupOrdersRepository
from src.services.base import BaseService

logger = logging.getLogger(__name__)


class PickupOrdersSyncService(BaseService):

    async def sync_orders(self, session: AsyncSession) -> dict:
        """
        Полная выгрузка заказов Самовывоз из WB API и сохранение в БД.
        """
        repo = PickupOrdersRepository(session)

        async with PickupOrdersCollector() as collector:
            response = await collector.get_orders()

        orders_data = [
            o.model_dump() if hasattr(o, "model_dump") else o
            for o in (response.orders or [])
        ]

        saved = await repo.upsert_many(orders_data)
        logger.info(f"Pickup orders synced: {saved} orders saved")
        return {"synced": saved, "source": "full"}

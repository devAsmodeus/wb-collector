"""Сервис Sync: FBS — Синхронизация сборочных заданий."""
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.fbs.orders import OrdersCollector
from src.repositories.fbs.orders import FbsOrdersRepository
from src.services.base import BaseService

logger = logging.getLogger(__name__)


class FbsOrdersSyncService(BaseService):

    async def sync_orders(self, session: AsyncSession) -> dict:
        """
        Полная выгрузка всех сборочных заданий FBS.
        Использует пагинацию по limit/offset: в каждом ответе приходит список заказов,
        цикл продолжается, пока API возвращает заказы.
        """
        repo = FbsOrdersRepository(session)
        all_orders: list[dict] = []

        async with OrdersCollector() as collector:
            offset = 0
            limit = 1000

            while True:
                response = await collector.get_orders(limit=limit, offset=offset)

                if not response.orders:
                    break

                for order in response.orders:
                    all_orders.append(order.model_dump() if hasattr(order, "model_dump") else order)

                if len(response.orders) < limit:
                    break

                offset += limit

        saved = await repo.upsert_many(all_orders)
        logger.info(f"FBS orders synced: {saved} orders saved")
        return {"synced": saved, "source": "full"}

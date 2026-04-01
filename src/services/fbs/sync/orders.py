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
        WB API v3 использует курсорную пагинацию через `next` (id последнего заказа).
        """
        repo = FbsOrdersRepository(session)
        all_orders: list[dict] = []

        async with OrdersCollector() as collector:
            next_cursor = 0
            limit = 1000

            while True:
                response = await collector.get_orders(limit=limit, next_cursor=next_cursor)

                if not response.orders:
                    break

                for order in response.orders:
                    all_orders.append(order.model_dump() if hasattr(order, "model_dump") else order)

                # WB API возвращает next в корне ответа (курсор для следующей страницы)
                new_cursor = response.next
                if not new_cursor or new_cursor == next_cursor:
                    break
                next_cursor = new_cursor

                if len(response.orders) < limit:
                    break

        saved = await repo.upsert_many(all_orders)
        logger.info(f"FBS orders synced: {saved} orders saved")
        return {"synced": saved, "source": "full"}

    async def sync_incremental(self, session: AsyncSession) -> dict:
        """
        Инкрементальная синхронизация — только новые заказы FBS начиная с max date в БД.
        Если БД пуста — делает полную выгрузку.
        """
        repo = FbsOrdersRepository(session)
        max_date = await repo.get_max_date()

        if not max_date:
            return await self.sync_orders(session)

        date_from = int(max_date.timestamp())
        all_orders: list[dict] = []

        async with OrdersCollector() as collector:
            next_cursor = 0
            limit = 1000

            while True:
                response = await collector.get_orders(
                    date_from=date_from, limit=limit, next_cursor=next_cursor,
                )

                if not response.orders:
                    break

                for order in response.orders:
                    all_orders.append(order.model_dump() if hasattr(order, "model_dump") else order)

                new_cursor = response.next
                if not new_cursor or new_cursor == next_cursor:
                    break
                next_cursor = new_cursor

                if len(response.orders) < limit:
                    break

        saved = await repo.upsert_many(all_orders)
        logger.info(f"FBS orders incremental sync: {saved} orders saved from {max_date}")
        return {
            "synced": saved,
            "source": "incremental",
            "from_date": max_date.isoformat(),
        }

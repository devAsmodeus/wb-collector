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
        Полная выгрузка ВСЕХ сборочных заданий FBS за все время.
        WB API v3 позволяет максимум 30 дней за один запрос,
        поэтому перебираем 30-дневные окна с самого начала (2 года назад).
        Курсорная пагинация через `next` (id последнего заказа).
        """
        from datetime import datetime, timedelta

        repo = FbsOrdersRepository(session)
        all_orders: list[dict] = []

        # Перебираем 30-дневные окна за последние 2 года
        now = datetime.utcnow()
        window_start = now - timedelta(days=730)  # 2 года назад

        async with OrdersCollector() as collector:
            while window_start < now:
                window_end = min(window_start + timedelta(days=30), now)
                date_from = int(window_start.timestamp())
                date_to = int(window_end.timestamp())

                next_cursor = 0
                limit = 1000

                while True:
                    response = await collector.get_orders(
                        limit=limit, next_cursor=next_cursor,
                        date_from=date_from, date_to=date_to,
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

                logger.info(f"FBS orders window {window_start.date()}..{window_end.date()}: +{len(all_orders)} total")
                window_start = window_end

        saved = await repo.upsert_many(all_orders)
        logger.info(f"FBS orders synced: {saved} orders saved (all time)")
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

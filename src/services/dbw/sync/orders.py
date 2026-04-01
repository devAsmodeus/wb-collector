"""Сервис Sync: DBW — Синхронизация заказов."""
import logging
from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.dbw.orders import DBWOrdersCollector
from src.exceptions import WBApiException
from src.repositories.dbw.orders import DbwOrdersRepository
from src.services.base import BaseService

logger = logging.getLogger(__name__)


class DBWOrdersSyncService(BaseService):

    async def sync_orders(self, session: AsyncSession, days_back: int = 30) -> dict:
        """Полная выгрузка заказов DBW из WB API и сохранение в БД.

        YAML: dateFrom и dateTo оба обязательны (unix timestamp), макс. 30 дней.
        """
        repo = DbwOrdersRepository(session)
        now = datetime.now(timezone.utc)
        date_from = int((now - timedelta(days=days_back)).timestamp())
        date_to = int(now.timestamp())

        try:
            async with DBWOrdersCollector() as collector:
                response = await collector.get_orders(date_from=date_from, date_to=date_to)
        except WBApiException as e:
            if e.status_code == 400:
                logger.info("DBW orders: схема не подключена или нет заказов")
                return {"synced": 0, "source": "full", "message": "Нет заказов DBW"}
            raise

        orders_data = [
            o.model_dump() if hasattr(o, "model_dump") else o
            for o in (response.orders or [])
        ]

        saved = await repo.upsert_many(orders_data)
        logger.info(f"DBW orders synced: {saved} orders saved")
        return {"synced": saved, "source": "full"}

    async def sync_incremental(self, session: AsyncSession) -> dict:
        """
        Инкрементальная синхронизация — только новые заказы DBW начиная с max date в БД.
        Если БД пуста — делает полную выгрузку.
        """
        repo = DbwOrdersRepository(session)
        max_date = await repo.get_max_date()

        if not max_date:
            return await self.sync_orders(session)

        date_from = int(max_date.timestamp())
        date_to = int(datetime.now(timezone.utc).timestamp())

        try:
            async with DBWOrdersCollector() as collector:
                response = await collector.get_orders(date_from=date_from, date_to=date_to)
        except WBApiException as e:
            if e.status_code == 400:
                logger.info("DBW orders incremental: схема не подключена или нет заказов")
                return {"synced": 0, "source": "incremental", "from_date": max_date.isoformat()}
            raise

        orders_data = [
            o.model_dump() if hasattr(o, "model_dump") else o
            for o in (response.orders or [])
        ]

        saved = await repo.upsert_many(orders_data)
        logger.info(f"DBW orders incremental sync: {saved} orders saved from {max_date}")
        return {
            "synced": saved,
            "source": "incremental",
            "from_date": max_date.isoformat(),
        }

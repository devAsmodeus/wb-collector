"""Сервис Sync: Отчёты — Синхронизация остатков, заказов, продаж в БД."""
import logging
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.reports.reports import ReportsCollector
from src.repositories.reports.stocks import StocksRepository
from src.repositories.reports.order_reports import OrderReportsRepository
from src.repositories.reports.sale_reports import SaleReportsRepository
from src.services.base import BaseService

logger = logging.getLogger(__name__)


def _default_date_from() -> str:
    """Дата год назад в формате YYYY-MM-DD."""
    return (datetime.utcnow() - timedelta(days=365)).strftime("%Y-%m-%d")


class ReportsSyncService(BaseService):

    async def sync_stocks(self, session: AsyncSession, date_from: str) -> dict:
        """Загружает остатки на складах и сохраняет в БД."""
        repo = StocksRepository(session)
        async with ReportsCollector() as collector:
            response = await collector.get_stocks(date_from)
        items = response if isinstance(response, list) else []
        saved = await repo.upsert_many(items)
        logger.info(f"Stocks synced: {saved} records")
        return {"synced": saved, "source": "stocks"}

    async def sync_orders(self, session: AsyncSession, date_from: str) -> dict:
        """Загружает заказы и сохраняет в БД."""
        repo = OrderReportsRepository(session)
        async with ReportsCollector() as collector:
            response = await collector.get_orders(date_from)
        items = response if isinstance(response, list) else []
        saved = await repo.upsert_many(items)
        logger.info(f"Orders synced: {saved} records")
        return {"synced": saved, "source": "orders"}

    async def sync_sales(self, session: AsyncSession, date_from: str) -> dict:
        """Загружает продажи/возвраты и сохраняет в БД."""
        repo = SaleReportsRepository(session)
        async with ReportsCollector() as collector:
            response = await collector.get_sales(date_from)
        items = response if isinstance(response, list) else []
        saved = await repo.upsert_many(items)
        logger.info(f"Sales synced: {saved} records")
        return {"synced": saved, "source": "sales"}

    async def sync_stocks_incremental(self, session: AsyncSession) -> dict:
        """
        Инкрементальная синхронизация остатков — начиная с max last_change_date в БД.
        Если БД пуста — делает полную выгрузку за год.
        """
        repo = StocksRepository(session)
        max_date = await repo.get_max_date()

        if not max_date:
            return await self.sync_stocks(session, _default_date_from())

        date_from = max_date.strftime("%Y-%m-%d")
        async with ReportsCollector() as collector:
            response = await collector.get_stocks(date_from)
        items = response if isinstance(response, list) else []
        saved = await repo.upsert_many(items)
        logger.info(f"Stocks incremental synced: {saved} records from {date_from}")
        return {
            "synced": saved,
            "source": "incremental",
            "from_date": date_from,
        }

    async def sync_orders_incremental(self, session: AsyncSession) -> dict:
        """
        Инкрементальная синхронизация заказов — начиная с max last_change_date в БД.
        Если БД пуста — делает полную выгрузку за год.
        """
        repo = OrderReportsRepository(session)
        max_date = await repo.get_max_date()

        if not max_date:
            return await self.sync_orders(session, _default_date_from())

        date_from = max_date.strftime("%Y-%m-%d")
        async with ReportsCollector() as collector:
            response = await collector.get_orders(date_from)
        items = response if isinstance(response, list) else []
        saved = await repo.upsert_many(items)
        logger.info(f"Orders incremental synced: {saved} records from {date_from}")
        return {
            "synced": saved,
            "source": "incremental",
            "from_date": date_from,
        }

    async def sync_sales_incremental(self, session: AsyncSession) -> dict:
        """
        Инкрементальная синхронизация продаж — начиная с max last_change_date в БД.
        Если БД пуста — делает полную выгрузку за год.
        """
        repo = SaleReportsRepository(session)
        max_date = await repo.get_max_date()

        if not max_date:
            return await self.sync_sales(session, _default_date_from())

        date_from = max_date.strftime("%Y-%m-%d")
        async with ReportsCollector() as collector:
            response = await collector.get_sales(date_from)
        items = response if isinstance(response, list) else []
        saved = await repo.upsert_many(items)
        logger.info(f"Sales incremental synced: {saved} records from {date_from}")
        return {
            "synced": saved,
            "source": "incremental",
            "from_date": date_from,
        }

"""Сервис Sync: Отчёты — Синхронизация остатков, заказов, продаж в БД."""
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.reports.reports import ReportsCollector
from src.repositories.reports.stocks import StocksRepository
from src.repositories.reports.order_reports import OrderReportsRepository
from src.repositories.reports.sale_reports import SaleReportsRepository
from src.services.base import BaseService

logger = logging.getLogger(__name__)


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

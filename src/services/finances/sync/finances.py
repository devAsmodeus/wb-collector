"""Сервис Sync: Финансы — Синхронизация финансового отчёта в БД."""
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.finances.finances import FinancesCollector
from src.repositories.finances.financial_reports import FinancialReportsRepository
from src.services.base import BaseService

logger = logging.getLogger(__name__)


class FinancesSyncService(BaseService):

    async def sync_financial_report(self, session: AsyncSession, date_from: str, date_to: str) -> dict:
        """
        Загружает финансовый отчёт с пагинацией по rrdid и сохраняет в БД.
        """
        repo = FinancialReportsRepository(session)
        all_items = []
        rrdid = 0
        limit = 100000

        async with FinancesCollector() as collector:
            while True:
                response = await collector.get_financial_report(date_from, date_to, limit=limit, rrdid=rrdid)
                items = response if isinstance(response, list) else []
                if not items:
                    break
                all_items.extend(items)
                last_rrd_id = items[-1].get("rrd_id", 0)
                if last_rrd_id <= rrdid:
                    break
                rrdid = last_rrd_id

        saved = await repo.upsert_many(all_items)
        logger.info(f"Financial report synced: {saved} records")
        return {"synced": saved, "source": "financial_report"}

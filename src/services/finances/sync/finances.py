"""Сервис Sync: Финансы — Синхронизация финансового отчёта в БД."""
import logging
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.finances.finances import FinancesCollector
from src.exceptions import WBApiException
from src.repositories.finances.financial_reports import FinancialReportsRepository
from src.services.base import BaseService

logger = logging.getLogger(__name__)


class FinancesSyncService(BaseService):

    async def sync_financial_report(self, session: AsyncSession, date_from: str, date_to: str) -> dict:
        """
        Загружает финансовый отчёт с пагинацией по rrdid и сохраняет в БД.
        WB возвращает 204 когда данных нет.
        """
        repo = FinancialReportsRepository(session)
        all_items = []
        rrdid = 0
        limit = 100000

        async with FinancesCollector() as collector:
            while True:
                try:
                    response = await collector.get_financial_report(date_from, date_to, limit=limit, rrdid=rrdid)
                except WBApiException as e:
                    if e.status_code == 204:
                        logger.info("Financial report: WB вернул 204 (нет данных за период)")
                        break
                    raise
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

    async def sync_financial_report_incremental(self, session: AsyncSession, date_from: str, date_to: str) -> dict:
        """
        Инкрементальная загрузка финансового отчёта.
        Начинает с max(rrd_id) из БД вместо 0, загружает только новые записи.
        Если БД пуста — fallback на полную синхронизацию.
        """
        repo = FinancialReportsRepository(session)
        max_rrd_id = await repo.get_max_rrd_id()

        if max_rrd_id is None:
            logger.info("Financial report incremental: no data in DB, falling back to full sync")
            result = await self.sync_financial_report(session, date_from, date_to)
            result["source"] = "incremental_fallback_full"
            return result

        all_items = []
        rrdid = max_rrd_id
        limit = 100000

        async with FinancesCollector() as collector:
            while True:
                try:
                    response = await collector.get_financial_report(date_from, date_to, limit=limit, rrdid=rrdid)
                except WBApiException as e:
                    if e.status_code == 204:
                        logger.info("Financial report incremental: WB вернул 204 (нет новых данных)")
                        break
                    raise
                items = response if isinstance(response, list) else []
                if not items:
                    break
                all_items.extend(items)
                last_rrd_id = items[-1].get("rrd_id", 0)
                if last_rrd_id <= rrdid:
                    break
                rrdid = last_rrd_id

        saved = await repo.upsert_many(all_items)
        logger.info(f"Financial report incremental synced: {saved} records (from rrd_id={max_rrd_id})")
        return {"synced": saved, "source": "incremental", "from_rrd_id": max_rrd_id}

"""Сервис Sync: Финансы — Синхронизация финансового отчёта с WB."""
import logging
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.finances.finances import FinancesCollector
from src.exceptions import WBApiException
from src.repositories.finances.financial_reports import FinancialReportsRepository
from src.services.base import BaseService

logger = logging.getLogger(__name__)


class FinancesSyncService(BaseService):

    async def sync_financial_report_historical(self, session: AsyncSession) -> dict:
        """
        Полный исторический дамп финансового отчёта за 2 года по неделям.
        Предназначен для первоначальной загрузки через Celery.
        Разбит на 7-дневные окна чтобы WB API не таймаутил на большом объёме.
        """
        repo = FinancialReportsRepository(session)
        total_saved = 0
        end = datetime.utcnow()
        # Берём 2 года назад, идём по неделям вперёд
        start = end - timedelta(days=730)
        current = start
        week_num = 0

        while current < end:
            week_num += 1
            date_from = current.strftime("%Y-%m-%d")
            date_to = min(current + timedelta(days=7), end).strftime("%Y-%m-%d")
            rrdid = 0

            async with FinancesCollector() as collector:
                while True:
                    try:
                        items = await collector.get_financial_report(
                            date_from, date_to, limit=100000, rrdid=rrdid
                        )
                    except WBApiException as e:
                        if e.status_code == 204:
                            break
                        logger.warning(f"Financial historical: week={week_num} error {e.status_code}")
                        break

                    if not items or not isinstance(items, list):
                        break

                    saved = await repo.upsert_many(items)
                    total_saved += saved
                    logger.info(
                        f"Financial historical: week={week_num} [{date_from}→{date_to}], "
                        f"rows={len(items)}, total={total_saved}"
                    )

                    last_rrd_id = items[-1].get("rrd_id", 0)
                    if last_rrd_id <= rrdid or len(items) < 100000:
                        break
                    rrdid = last_rrd_id

            current += timedelta(days=7)

        logger.info(f"Financial historical sync done: {total_saved} total ({week_num} weeks)")
        return {"synced": total_saved, "source": "historical", "weeks": week_num}

    async def sync_financial_report(self, session: AsyncSession, date_from: str, date_to: str) -> dict:
        """
        Загружает финансовый отчёт с пагинацией по rrdid.
        Upsert делается после каждой страницы WB чтобы не держать всё в памяти.
        WB возвращает 204 когда данные закончились.
        """
        repo = FinancialReportsRepository(session)
        rrdid = 0
        limit = 100000
        total_saved = 0
        page = 0

        async with FinancesCollector() as collector:
            while True:
                page += 1
                try:
                    items = await collector.get_financial_report(
                        date_from, date_to, limit=limit, rrdid=rrdid
                    )
                except WBApiException as e:
                    if e.status_code == 204:
                        logger.info(f"Financial report: WB вернул 204 (нет данных за период), page={page}")
                        break
                    raise

                if not items or not isinstance(items, list):
                    break

                logger.info(f"Financial report: page={page}, rrdid={rrdid}, got {len(items)} rows")

                # Upsert сразу — не накапливаем всё в памяти
                saved = await repo.upsert_many(items)
                total_saved += saved

                last_rrd_id = items[-1].get("rrd_id", 0)
                if last_rrd_id <= rrdid:
                    break
                rrdid = last_rrd_id

                # Если вернулось меньше лимита — данные закончились
                if len(items) < limit:
                    break

        logger.info(f"Financial report synced: {total_saved} records total ({page} pages)")
        return {"synced": total_saved, "source": "financial_report", "pages": page}

    async def sync_financial_report_incremental(self, session: AsyncSession, date_from: str, date_to: str) -> dict:
        """
        Инкрементальная синхронизация финансового отчёта.
        Стартует с max(rrd_id) из БД. Если БД пуста — fallback на полный sync.
        """
        repo = FinancialReportsRepository(session)
        max_rrd_id = await repo.get_max_rrd_id()

        if max_rrd_id is None:
            logger.info("Financial report incremental: no data in DB, falling back to full sync")
            result = await self.sync_financial_report(session, date_from, date_to)
            result["source"] = "incremental_fallback_full"
            return result

        rrdid = max_rrd_id
        limit = 100000
        total_saved = 0
        page = 0

        async with FinancesCollector() as collector:
            while True:
                page += 1
                try:
                    items = await collector.get_financial_report(
                        date_from, date_to, limit=limit, rrdid=rrdid
                    )
                except WBApiException as e:
                    if e.status_code == 204:
                        logger.info(f"Financial report incremental: WB 204 (нет новых данных), page={page}")
                        break
                    raise

                if not items or not isinstance(items, list):
                    break

                logger.info(f"Financial report incremental: page={page}, rrdid={rrdid}, got {len(items)} rows")

                saved = await repo.upsert_many(items)
                total_saved += saved

                last_rrd_id = items[-1].get("rrd_id", 0)
                if last_rrd_id <= rrdid:
                    break
                rrdid = last_rrd_id

                if len(items) < limit:
                    break

        logger.info(
            f"Financial report incremental synced: {total_saved} records ({page} pages), "
            f"from_rrd_id={max_rrd_id}"
        )
        return {
            "synced": total_saved,
            "source": "incremental",
            "from_rrd_id": max_rrd_id,
            "pages": page,
        }

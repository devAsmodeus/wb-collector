"""Сервис Sync: Аналитика — Остатки по группам."""
import logging
from datetime import date, datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.analytics import AnalyticsCollector
from src.repositories.analytics.stocks import StocksRepository
from src.services.base import BaseService

logger = logging.getLogger(__name__)


class StocksSyncService(BaseService):

    async def _fetch_stocks_data(
        self,
        collector: AnalyticsCollector,
        start_date: str,
        end_date: str,
    ) -> list[dict]:
        """Загружает данные по остаткам из WB API."""
        payload = {
            "startDate": start_date,
            "endDate": end_date,
            "timezone": "Europe/Moscow",
        }

        try:
            response = await collector.get_stocks_groups(payload)
        except Exception as e:
            logger.error(f"Stocks sync: error fetching data: {e}")
            return []

        data = response.get("data", response)
        groups = data.get("groups", data) if isinstance(data, dict) else data

        if not isinstance(groups, list):
            groups = []

        all_rows = []
        for group in groups:
            metrics = group.get("metrics", {})
            items = group.get("items", [])

            for item in items:
                item_metrics = item.get("metrics", {})
                row = {
                    "nm_id": item.get("nmId") or item.get("nmID"),
                    "vendor_code": item.get("vendorCode"),
                    "brand_name": group.get("brandName") or item.get("brandName"),
                    "subject_name": group.get("subjectName") or item.get("subjectName"),
                    "orders_count": item_metrics.get("ordersCount") or metrics.get("ordersCount"),
                    "orders_sum": item_metrics.get("ordersSum") or metrics.get("ordersSum"),
                    "avg_orders": item_metrics.get("avgOrders") or metrics.get("avgOrders"),
                    "buyout_count": item_metrics.get("buyoutCount") or metrics.get("buyoutCount"),
                    "buyout_sum": item_metrics.get("buyoutSum") or metrics.get("buyoutSum"),
                    "buyout_percent": item_metrics.get("buyoutPercent") or metrics.get("buyoutPercent"),
                    "stock_count": item_metrics.get("stockCount") or metrics.get("stockCount"),
                    "stock_sum": item_metrics.get("stockSum") or metrics.get("stockSum"),
                    "days_on_site": item.get("daysOnSite"),
                    "period_start": date.fromisoformat(start_date),
                    "period_end": date.fromisoformat(end_date),
                    "raw_data": item,
                    "fetched_at": datetime.utcnow(),
                }

                if row["nm_id"] is not None:
                    all_rows.append(row)

        return all_rows

    async def sync_stocks_full(self, session: AsyncSession) -> dict:
        """
        Полная выгрузка остатков за последние 30 дней.
        """
        repo = StocksRepository(session)

        end_date = date.today()
        start_date = end_date - timedelta(days=30)

        async with AnalyticsCollector() as collector:
            all_rows = await self._fetch_stocks_data(
                collector,
                start_date.isoformat(),
                end_date.isoformat(),
            )

        saved = await repo.upsert_many(all_rows)
        logger.info(f"Stocks synced: {saved} records saved (full)")
        return {"synced": saved, "source": "full"}

    async def sync_stocks_incremental(self, session: AsyncSession) -> dict:
        """
        Инкрементальная синхронизация остатков.
        Загружает данные с max(period_start) из БД по текущий день.
        Если БД пуста — fallback на полную синхронизацию.
        """
        repo = StocksRepository(session)
        max_period = await repo.get_max_period_start()

        if max_period is None:
            logger.info("Stocks incremental: no data in DB, falling back to full sync")
            result = await self.sync_stocks_full(session)
            result["source"] = "incremental_fallback_full"
            return result

        start_date = max_period
        end_date = date.today()

        async with AnalyticsCollector() as collector:
            all_rows = await self._fetch_stocks_data(
                collector,
                start_date.isoformat(),
                end_date.isoformat(),
            )

        saved = await repo.upsert_many(all_rows)
        logger.info(f"Stocks incremental synced: {saved} records (from_date={max_period.isoformat()})")
        return {"synced": saved, "source": "incremental", "from_date": max_period.isoformat()}

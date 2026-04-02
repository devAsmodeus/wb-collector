"""Сервис Sync: Аналитика — Воронка продаж по артикулам."""
import logging
from datetime import date, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.analytics import AnalyticsCollector
from src.models.products import WbCard
from src.repositories.analytics.funnel import FunnelRepository
from src.services.base import BaseService

logger = logging.getLogger(__name__)

# WB API ограничение: максимум 20 nmID за один запрос
_FUNNEL_BATCH_SIZE = 20


class FunnelSyncService(BaseService):

    async def _get_all_nm_ids(self, session: AsyncSession) -> list[int]:
        """Получает все nm_id из таблицы wb_cards."""
        result = await session.execute(select(WbCard.nm_id).order_by(WbCard.nm_id))
        return list(result.scalars().all())

    async def sync_funnel_full(self, session: AsyncSession) -> dict:
        """
        Полная выгрузка воронки продаж за последние 30 дней.
        Получает nm_id из wb_cards и запрашивает воронку батчами по 20.
        """
        repo = FunnelRepository(session)
        nm_ids = await self._get_all_nm_ids(session)

        if not nm_ids:
            logger.warning("Funnel sync: no nm_ids in wb_cards, nothing to sync")
            return {"synced": 0, "source": "full", "error": "no nm_ids in wb_cards"}

        end_date = date.today()
        start_date = end_date - timedelta(days=30)

        all_rows = []
        async with AnalyticsCollector() as collector:
            for i in range(0, len(nm_ids), _FUNNEL_BATCH_SIZE):
                batch_ids = nm_ids[i: i + _FUNNEL_BATCH_SIZE]
                payload = {
                    "nmIds": batch_ids,
                    "selectedPeriod": {
                        "start": start_date.isoformat(),
                        "end": end_date.isoformat(),
                    },
                    "skipDeletedNm": False,
                    "orderBy": {"field": "orderCount", "mode": "desc"},
                    "limit": _FUNNEL_BATCH_SIZE,
                    "offset": 0,
                }

                try:
                    response = await collector.get_funnel_products(payload)
                except Exception as e:
                    logger.error(f"Funnel sync: error for batch {i}: {e}")
                    continue

                data = response.get("data", {})
                products = data.get("products", [])

                for item in products:
                    product = item.get("product", {})
                    statistic = item.get("statistic", {})
                    selected = statistic.get("selected", {})
                    period = selected.get("period", {})
                    conversions = selected.get("conversions")

                    period_start = period.get("start")
                    if not period_start:
                        continue

                    row = {
                        "nm_id": product.get("nmId"),
                        "vendor_code": product.get("vendorCode"),
                        "brand_name": product.get("brandName"),
                        "subject_name": product.get("subjectName"),
                        "date": date.fromisoformat(period_start),
                        "opens_count": selected.get("openCount"),
                        "add_to_cart_count": selected.get("cartCount"),
                        "orders_count": selected.get("orderCount"),
                        "orders_sum_rub": selected.get("orderSum"),
                        "buyouts_count": selected.get("buyoutCount"),
                        "buyouts_sum_rub": selected.get("buyoutSum"),
                        "cancel_count": selected.get("cancelCount"),
                        "cancel_sum_rub": selected.get("cancelSum"),
                        "avg_price_rub": selected.get("avgPrice"),
                        "avg_orders_count_per_day": selected.get("avgOrdersCountPerDay"),
                        "conversions": conversions,
                        "raw_data": item,
                        "fetched_at": datetime.utcnow(),
                    }

                    if row["nm_id"] is not None:
                        all_rows.append(row)

        saved = await repo.upsert_many(all_rows)
        logger.info(f"Funnel synced: {saved} records saved (full)")
        return {"synced": saved, "source": "full"}

    async def sync_funnel_incremental(self, session: AsyncSession) -> dict:
        """
        Инкрементальная синхронизация воронки продаж.
        Загружает данные с max(date) из БД по текущий день.
        Если БД пуста — fallback на полную синхронизацию.
        """
        repo = FunnelRepository(session)
        max_date = await repo.get_max_date()

        if max_date is None:
            logger.info("Funnel incremental: no data in DB, falling back to full sync")
            result = await self.sync_funnel_full(session)
            result["source"] = "incremental_fallback_full"
            return result

        nm_ids = await self._get_all_nm_ids(session)
        if not nm_ids:
            return {"synced": 0, "source": "incremental", "error": "no nm_ids in wb_cards"}

        start_date = max_date
        end_date = date.today()

        all_rows = []
        async with AnalyticsCollector() as collector:
            for i in range(0, len(nm_ids), _FUNNEL_BATCH_SIZE):
                batch_ids = nm_ids[i: i + _FUNNEL_BATCH_SIZE]
                payload = {
                    "nmIds": batch_ids,
                    "selectedPeriod": {
                        "start": start_date.isoformat(),
                        "end": end_date.isoformat(),
                    },
                    "skipDeletedNm": False,
                    "orderBy": {"field": "orderCount", "mode": "desc"},
                    "limit": _FUNNEL_BATCH_SIZE,
                    "offset": 0,
                }

                try:
                    response = await collector.get_funnel_products(payload)
                except Exception as e:
                    logger.error(f"Funnel incremental: error for batch {i}: {e}")
                    continue

                data = response.get("data", {})
                products = data.get("products", [])

                for item in products:
                    product = item.get("product", {})
                    statistic = item.get("statistic", {})
                    selected = statistic.get("selected", {})
                    period = selected.get("period", {})
                    conversions = selected.get("conversions")

                    period_start = period.get("start")
                    if not period_start:
                        continue

                    row = {
                        "nm_id": product.get("nmId"),
                        "vendor_code": product.get("vendorCode"),
                        "brand_name": product.get("brandName"),
                        "subject_name": product.get("subjectName"),
                        "date": date.fromisoformat(period_start),
                        "opens_count": selected.get("openCount"),
                        "add_to_cart_count": selected.get("cartCount"),
                        "orders_count": selected.get("orderCount"),
                        "orders_sum_rub": selected.get("orderSum"),
                        "buyouts_count": selected.get("buyoutCount"),
                        "buyouts_sum_rub": selected.get("buyoutSum"),
                        "cancel_count": selected.get("cancelCount"),
                        "cancel_sum_rub": selected.get("cancelSum"),
                        "avg_price_rub": selected.get("avgPrice"),
                        "avg_orders_count_per_day": selected.get("avgOrdersCountPerDay"),
                        "conversions": conversions,
                        "raw_data": item,
                        "fetched_at": datetime.utcnow(),
                    }

                    if row["nm_id"] is not None:
                        all_rows.append(row)

        saved = await repo.upsert_many(all_rows)
        logger.info(f"Funnel incremental synced: {saved} records (from_date={max_date.isoformat()})")
        return {"synced": saved, "source": "incremental", "from_date": max_date.isoformat()}


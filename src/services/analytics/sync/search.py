"""Сервис Sync: Аналитика — Поисковые запросы по товарам."""
import logging
from datetime import date, datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.analytics import AnalyticsCollector
from src.repositories.analytics.search import SearchRepository
from src.services.base import BaseService

logger = logging.getLogger(__name__)

# WB API ограничение: skip + take <= 10000
_SEARCH_MAX_OFFSET = 10000
_SEARCH_PAGE_SIZE = 200


class SearchSyncService(BaseService):

    async def _fetch_search_data(
        self,
        collector: AnalyticsCollector,
        start_date: str,
        end_date: str,
    ) -> list[dict]:
        """Загружает все страницы поисковых запросов из WB API с пагинацией."""
        all_rows = []
        offset = 0

        while offset < _SEARCH_MAX_OFFSET:
            payload = {
                "currentPeriod": {
                    "start": start_date,
                    "end": end_date,
                },
                "positionCluster": "all",
                "orderBy": {"field": "avgPosition", "mode": "desc"},
                "limit": _SEARCH_PAGE_SIZE,
                "offset": offset,
            }

            try:
                response = await collector.get_search_report(payload)
            except Exception as e:
                logger.error(f"Search sync: error at offset {offset}: {e}")
                break

            # Ответ — CSV-подобная структура или JSON с items
            # Пробуем обработать как JSON с data/items
            data = response.get("data", response)
            items = data.get("items", []) if isinstance(data, dict) else []

            if not items:
                break

            for item in items:
                row = {
                    "nm_id": item.get("nmId") or item.get("nmID"),
                    "text": item.get("text"),
                    "frequency": self._extract_current(item.get("frequency")),
                    "avg_position": self._extract_current(item.get("avgPosition")),
                    "median_position": self._extract_current(item.get("medianPosition")),
                    "opens_count": self._extract_current(item.get("openCard")),
                    "add_to_cart_count": self._extract_current(item.get("addToCart")),
                    "orders_count": self._extract_current(item.get("orders")),
                    "orders_sum_rub": None,
                    "period_start": date.fromisoformat(start_date),
                    "period_end": date.fromisoformat(end_date),
                    "raw_data": item,
                    "fetched_at": datetime.utcnow(),
                }

                if row["nm_id"] is not None:
                    all_rows.append(row)

            if len(items) < _SEARCH_PAGE_SIZE:
                break

            offset += _SEARCH_PAGE_SIZE

        return all_rows

    @staticmethod
    def _extract_current(value) -> int | float | None:
        """Извлекает .current из вложенного объекта {current: N, dynamics: N} или возвращает как есть."""
        if value is None:
            return None
        if isinstance(value, dict):
            return value.get("current")
        return value

    async def sync_search_full(self, session: AsyncSession) -> dict:
        """
        Полная выгрузка поисковых запросов за последние 7 дней.
        Пагинация: skip + take <= 10000.
        """
        repo = SearchRepository(session)

        end_date = date.today()
        start_date = end_date - timedelta(days=7)

        async with AnalyticsCollector() as collector:
            all_rows = await self._fetch_search_data(
                collector,
                start_date.isoformat(),
                end_date.isoformat(),
            )

        saved = await repo.upsert_many(all_rows)
        logger.info(f"Search synced: {saved} records saved (full)")
        return {"synced": saved, "source": "full"}

    async def sync_search_incremental(self, session: AsyncSession) -> dict:
        """
        Инкрементальная синхронизация поисковых запросов.
        Загружает данные с max(period_start) из БД по текущий день.
        Если БД пуста — fallback на полную синхронизацию.
        """
        repo = SearchRepository(session)
        max_period = await repo.get_max_period_start()

        if max_period is None:
            logger.info("Search incremental: no data in DB, falling back to full sync")
            result = await self.sync_search_full(session)
            result["source"] = "incremental_fallback_full"
            return result

        start_date = max_period
        end_date = date.today()

        async with AnalyticsCollector() as collector:
            all_rows = await self._fetch_search_data(
                collector,
                start_date.isoformat(),
                end_date.isoformat(),
            )

        saved = await repo.upsert_many(all_rows)
        logger.info(f"Search incremental synced: {saved} records (from_date={max_period.isoformat()})")
        return {"synced": saved, "source": "incremental", "from_date": max_period.isoformat()}

"""Репозиторий: Аналитика — Остатки по группам."""
from datetime import date, datetime

from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.analytics import AnalyticsStocksGroup


class StocksRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def upsert_many(self, rows: list[dict]) -> int:
        """Вставляет или обновляет записи остатков. Возвращает кол-во обработанных записей."""
        if not rows:
            return 0
        stmt = insert(AnalyticsStocksGroup).values(rows)
        stmt = stmt.on_conflict_do_update(
            constraint="uq_stocks_nm_id_period",
            set_={
                "vendor_code": stmt.excluded.vendor_code,
                "brand_name": stmt.excluded.brand_name,
                "subject_name": stmt.excluded.subject_name,
                "orders_count": stmt.excluded.orders_count,
                "orders_sum": stmt.excluded.orders_sum,
                "avg_orders": stmt.excluded.avg_orders,
                "buyout_count": stmt.excluded.buyout_count,
                "buyout_sum": stmt.excluded.buyout_sum,
                "buyout_percent": stmt.excluded.buyout_percent,
                "stock_count": stmt.excluded.stock_count,
                "stock_sum": stmt.excluded.stock_sum,
                "days_on_site": stmt.excluded.days_on_site,
                "period_end": stmt.excluded.period_end,
                "raw_data": stmt.excluded.raw_data,
                "fetched_at": stmt.excluded.fetched_at,
            },
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return len(rows)

    async def get_max_period_start(self) -> date | None:
        """Возвращает максимальную дату начала периода для инкрементальной синхронизации."""
        result = await self._session.execute(select(func.max(AnalyticsStocksGroup.period_start)))
        return result.scalar_one_or_none()

    async def count(self) -> int:
        """Возвращает общее количество записей в таблице."""
        result = await self._session.execute(select(func.count()).select_from(AnalyticsStocksGroup))
        return result.scalar_one()

    async def get_all(self, limit: int = 100, offset: int = 0) -> list[AnalyticsStocksGroup]:
        """Возвращает записи остатков с пагинацией."""
        result = await self._session.execute(
            select(AnalyticsStocksGroup)
            .order_by(AnalyticsStocksGroup.period_start.desc(), AnalyticsStocksGroup.nm_id)
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def get_by_nm_id(self, nm_id: int, limit: int = 100, offset: int = 0) -> list[AnalyticsStocksGroup]:
        """Возвращает остатки по nm_id."""
        result = await self._session.execute(
            select(AnalyticsStocksGroup)
            .where(AnalyticsStocksGroup.nm_id == nm_id)
            .order_by(AnalyticsStocksGroup.period_start.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def get_filtered(
        self,
        nm_id: int | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[AnalyticsStocksGroup]:
        """Возвращает остатки с фильтрацией."""
        query = select(AnalyticsStocksGroup)
        if nm_id is not None:
            query = query.where(AnalyticsStocksGroup.nm_id == nm_id)
        if date_from is not None:
            query = query.where(AnalyticsStocksGroup.period_start >= date_from)
        if date_to is not None:
            query = query.where(AnalyticsStocksGroup.period_start <= date_to)
        query = query.order_by(AnalyticsStocksGroup.period_start.desc(), AnalyticsStocksGroup.nm_id).limit(limit).offset(offset)
        result = await self._session.execute(query)
        return list(result.scalars().all())

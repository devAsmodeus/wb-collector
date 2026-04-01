"""Репозиторий: Аналитика — Поисковые запросы."""
from datetime import date, datetime

from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.analytics import AnalyticsSearchQuery


class SearchRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def upsert_many(self, rows: list[dict]) -> int:
        """Вставляет или обновляет записи поисковых запросов. Возвращает кол-во обработанных записей."""
        if not rows:
            return 0
        stmt = insert(AnalyticsSearchQuery).values(rows)
        stmt = stmt.on_conflict_do_update(
            constraint="uq_search_nm_text_period",
            set_={
                "frequency": stmt.excluded.frequency,
                "avg_position": stmt.excluded.avg_position,
                "median_position": stmt.excluded.median_position,
                "opens_count": stmt.excluded.opens_count,
                "add_to_cart_count": stmt.excluded.add_to_cart_count,
                "orders_count": stmt.excluded.orders_count,
                "orders_sum_rub": stmt.excluded.orders_sum_rub,
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
        result = await self._session.execute(select(func.max(AnalyticsSearchQuery.period_start)))
        return result.scalar_one_or_none()

    async def count(self) -> int:
        """Возвращает общее количество записей в таблице."""
        result = await self._session.execute(select(func.count()).select_from(AnalyticsSearchQuery))
        return result.scalar_one()

    async def get_all(self, limit: int = 100, offset: int = 0) -> list[AnalyticsSearchQuery]:
        """Возвращает записи поисковых запросов с пагинацией."""
        result = await self._session.execute(
            select(AnalyticsSearchQuery)
            .order_by(AnalyticsSearchQuery.period_start.desc(), AnalyticsSearchQuery.nm_id)
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def get_by_nm_id(self, nm_id: int, limit: int = 100, offset: int = 0) -> list[AnalyticsSearchQuery]:
        """Возвращает поисковые запросы по nm_id."""
        result = await self._session.execute(
            select(AnalyticsSearchQuery)
            .where(AnalyticsSearchQuery.nm_id == nm_id)
            .order_by(AnalyticsSearchQuery.period_start.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def get_filtered(
        self,
        nm_id: int | None = None,
        text: str | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[AnalyticsSearchQuery]:
        """Возвращает поисковые запросы с фильтрацией."""
        query = select(AnalyticsSearchQuery)
        if nm_id is not None:
            query = query.where(AnalyticsSearchQuery.nm_id == nm_id)
        if text is not None:
            query = query.where(AnalyticsSearchQuery.text.ilike(f"%{text}%"))
        if date_from is not None:
            query = query.where(AnalyticsSearchQuery.period_start >= date_from)
        if date_to is not None:
            query = query.where(AnalyticsSearchQuery.period_start <= date_to)
        query = query.order_by(AnalyticsSearchQuery.period_start.desc(), AnalyticsSearchQuery.nm_id).limit(limit).offset(offset)
        result = await self._session.execute(query)
        return list(result.scalars().all())

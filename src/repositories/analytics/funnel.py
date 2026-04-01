"""Репозиторий: Аналитика — Воронка продаж."""
from datetime import date, datetime

from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.analytics import AnalyticsFunnelProduct


class FunnelRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def upsert_many(self, rows: list[dict]) -> int:
        """Вставляет или обновляет записи воронки продаж. Возвращает кол-во обработанных записей."""
        if not rows:
            return 0
        stmt = insert(AnalyticsFunnelProduct).values(rows)
        stmt = stmt.on_conflict_do_update(
            constraint="uq_funnel_nm_id_date",
            set_={
                "vendor_code": stmt.excluded.vendor_code,
                "brand_name": stmt.excluded.brand_name,
                "subject_name": stmt.excluded.subject_name,
                "opens_count": stmt.excluded.opens_count,
                "add_to_cart_count": stmt.excluded.add_to_cart_count,
                "orders_count": stmt.excluded.orders_count,
                "orders_sum_rub": stmt.excluded.orders_sum_rub,
                "buyouts_count": stmt.excluded.buyouts_count,
                "buyouts_sum_rub": stmt.excluded.buyouts_sum_rub,
                "cancel_count": stmt.excluded.cancel_count,
                "cancel_sum_rub": stmt.excluded.cancel_sum_rub,
                "avg_price_rub": stmt.excluded.avg_price_rub,
                "avg_orders_count_per_day": stmt.excluded.avg_orders_count_per_day,
                "conversions": stmt.excluded.conversions,
                "raw_data": stmt.excluded.raw_data,
                "fetched_at": stmt.excluded.fetched_at,
            },
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return len(rows)

    async def get_max_date(self) -> date | None:
        """Возвращает максимальную дату из таблицы для инкрементальной синхронизации."""
        result = await self._session.execute(select(func.max(AnalyticsFunnelProduct.date)))
        return result.scalar_one_or_none()

    async def count(self) -> int:
        """Возвращает общее количество записей в таблице."""
        result = await self._session.execute(select(func.count()).select_from(AnalyticsFunnelProduct))
        return result.scalar_one()

    async def get_all(self, limit: int = 100, offset: int = 0) -> list[AnalyticsFunnelProduct]:
        """Возвращает записи воронки с пагинацией."""
        result = await self._session.execute(
            select(AnalyticsFunnelProduct)
            .order_by(AnalyticsFunnelProduct.date.desc(), AnalyticsFunnelProduct.nm_id)
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def get_by_nm_id(self, nm_id: int, limit: int = 100, offset: int = 0) -> list[AnalyticsFunnelProduct]:
        """Возвращает записи воронки по nm_id."""
        result = await self._session.execute(
            select(AnalyticsFunnelProduct)
            .where(AnalyticsFunnelProduct.nm_id == nm_id)
            .order_by(AnalyticsFunnelProduct.date.desc())
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
    ) -> list[AnalyticsFunnelProduct]:
        """Возвращает записи воронки с фильтрацией."""
        query = select(AnalyticsFunnelProduct)
        if nm_id is not None:
            query = query.where(AnalyticsFunnelProduct.nm_id == nm_id)
        if date_from is not None:
            query = query.where(AnalyticsFunnelProduct.date >= date_from)
        if date_to is not None:
            query = query.where(AnalyticsFunnelProduct.date <= date_to)
        query = query.order_by(AnalyticsFunnelProduct.date.desc(), AnalyticsFunnelProduct.nm_id).limit(limit).offset(offset)
        result = await self._session.execute(query)
        return list(result.scalars().all())

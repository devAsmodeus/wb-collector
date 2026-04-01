"""Сервис DB: Аналитика — Поисковые запросы из БД."""
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.analytics.search import SearchRepository
from src.services.base import BaseService


class SearchDbService(BaseService):

    async def get_search_queries(
        self,
        session: AsyncSession,
        nm_id: int | None = None,
        text: str | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Возвращает поисковые запросы из БД с фильтрацией."""
        repo = SearchRepository(session)
        total = await repo.count()
        items = await repo.get_filtered(
            nm_id=nm_id,
            text=text,
            date_from=date_from,
            date_to=date_to,
            limit=limit,
            offset=offset,
        )
        return {
            "data": [
                {
                    "nm_id": r.nm_id,
                    "text": r.text,
                    "frequency": r.frequency,
                    "avg_position": float(r.avg_position) if r.avg_position is not None else None,
                    "median_position": float(r.median_position) if r.median_position is not None else None,
                    "opens_count": r.opens_count,
                    "add_to_cart_count": r.add_to_cart_count,
                    "orders_count": r.orders_count,
                    "orders_sum_rub": float(r.orders_sum_rub) if r.orders_sum_rub is not None else None,
                    "period_start": r.period_start.isoformat() if r.period_start else None,
                    "period_end": r.period_end.isoformat() if r.period_end else None,
                    "fetched_at": r.fetched_at.isoformat() if r.fetched_at else None,
                }
                for r in items
            ],
            "total": total,
            "limit": limit,
            "offset": offset,
        }

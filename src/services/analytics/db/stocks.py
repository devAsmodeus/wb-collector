"""Сервис DB: Аналитика — Остатки по группам из БД."""
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.analytics.stocks import StocksRepository
from src.services.base import BaseService


class StocksDbService(BaseService):

    async def get_stocks(
        self,
        session: AsyncSession,
        nm_id: int | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Возвращает остатки по группам из БД с фильтрацией."""
        repo = StocksRepository(session)
        total = await repo.count()
        items = await repo.get_filtered(
            nm_id=nm_id,
            date_from=date_from,
            date_to=date_to,
            limit=limit,
            offset=offset,
        )
        return {
            "data": [
                {
                    "nm_id": r.nm_id,
                    "vendor_code": r.vendor_code,
                    "brand_name": r.brand_name,
                    "subject_name": r.subject_name,
                    "orders_count": r.orders_count,
                    "orders_sum": float(r.orders_sum) if r.orders_sum is not None else None,
                    "avg_orders": float(r.avg_orders) if r.avg_orders is not None else None,
                    "buyout_count": r.buyout_count,
                    "buyout_sum": float(r.buyout_sum) if r.buyout_sum is not None else None,
                    "buyout_percent": r.buyout_percent,
                    "stock_count": r.stock_count,
                    "stock_sum": float(r.stock_sum) if r.stock_sum is not None else None,
                    "days_on_site": r.days_on_site,
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

"""Сервис DB: Аналитика — Воронка продаж из БД."""
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.analytics.funnel import FunnelRepository
from src.services.base import BaseService


class FunnelDbService(BaseService):

    async def get_funnel(
        self,
        session: AsyncSession,
        nm_id: int | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Возвращает данные воронки продаж из БД с фильтрацией."""
        repo = FunnelRepository(session)
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
                    "date": r.date.isoformat() if r.date else None,
                    "opens_count": r.opens_count,
                    "add_to_cart_count": r.add_to_cart_count,
                    "orders_count": r.orders_count,
                    "orders_sum_rub": float(r.orders_sum_rub) if r.orders_sum_rub is not None else None,
                    "buyouts_count": r.buyouts_count,
                    "buyouts_sum_rub": float(r.buyouts_sum_rub) if r.buyouts_sum_rub is not None else None,
                    "cancel_count": r.cancel_count,
                    "cancel_sum_rub": float(r.cancel_sum_rub) if r.cancel_sum_rub is not None else None,
                    "avg_price_rub": float(r.avg_price_rub) if r.avg_price_rub is not None else None,
                    "avg_orders_count_per_day": float(r.avg_orders_count_per_day) if r.avg_orders_count_per_day is not None else None,
                    "conversions": r.conversions,
                    "fetched_at": r.fetched_at.isoformat() if r.fetched_at else None,
                }
                for r in items
            ],
            "total": total,
            "limit": limit,
            "offset": offset,
        }

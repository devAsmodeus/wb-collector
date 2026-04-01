"""Сервис DB: FBS — Чтение сборочных заданий из БД."""
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.fbs.orders import FbsOrdersRepository
from src.services.base import BaseService


class FbsOrdersDbService(BaseService):

    async def get_orders(
        self,
        session: AsyncSession,
        date_from: str | None = None,
        date_to: str | None = None,
        status: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Возвращает сборочные задания FBS из БД с фильтрацией."""
        repo = FbsOrdersRepository(session)
        total = await repo.count()
        items = await repo.get_filtered(
            date_from=date_from,
            date_to=date_to,
            status=status,
            limit=limit,
            offset=offset,
        )
        return {
            "data": [
                {
                    "order_id": o.order_id,
                    "order_uid": o.order_uid,
                    "date": o.date.isoformat() if o.date else None,
                    "last_change_date": o.last_change_date.isoformat() if o.last_change_date else None,
                    "warehouse_name": o.warehouse_name,
                    "country_name": o.country_name,
                    "region_name": o.region_name,
                    "article": o.article,
                    "nm_id": o.nm_id,
                    "subject": o.subject,
                    "category": o.category,
                    "brand": o.brand,
                    "name": o.name,
                    "tech_size": o.tech_size,
                    "total_price": float(o.total_price) if o.total_price else None,
                    "discount_percent": o.discount_percent,
                    "finished_price": float(o.finished_price) if o.finished_price else None,
                    "is_cancel": o.is_cancel,
                    "supplier_status": o.supplier_status,
                    "wb_status": o.wb_status,
                    "fetched_at": o.fetched_at.isoformat() if o.fetched_at else None,
                }
                for o in items
            ],
            "total": total,
            "limit": limit,
            "offset": offset,
        }

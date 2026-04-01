"""Сервис DB: DBW — Чтение заказов из БД."""
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.dbw.orders import DbwOrdersRepository
from src.services.base import BaseService


class DBWOrdersDbService(BaseService):

    async def get_orders(
        self,
        session: AsyncSession,
        date_from: str | None = None,
        date_to: str | None = None,
        status: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Возвращает заказы DBW из БД с фильтрацией."""
        repo = DbwOrdersRepository(session)
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
                    "article": o.article,
                    "nm_id": o.nm_id,
                    "brand": o.brand,
                    "name": o.name,
                    "total_price": float(o.total_price) if o.total_price else None,
                    "finished_price": float(o.finished_price) if o.finished_price else None,
                    "supplier_status": o.supplier_status,
                    "wb_status": o.wb_status,
                    "is_cancel": o.is_cancel,
                    "fetched_at": o.fetched_at.isoformat() if o.fetched_at else None,
                }
                for o in items
            ],
            "total": total,
            "limit": limit,
            "offset": offset,
        }

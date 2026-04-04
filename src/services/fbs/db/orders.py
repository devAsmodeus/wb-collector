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
        repo = FbsOrdersRepository(session)
        total = await repo.count()
        items = await repo.get_filtered(
            date_from=date_from,
            date_to=date_to,
            delivery_type=status,
            limit=limit,
            offset=offset,
        )
        return {
            "data": [
                {
                    "order_id":        o.order_id,
                    "order_uid":       o.order_uid,
                    "rid":             o.rid,
                    "created_at":      o.created_at.isoformat() if o.created_at else None,
                    "article":         o.article,
                    "color_code":      o.color_code,
                    "nm_id":           o.nm_id,
                    "chrt_id":         o.chrt_id,
                    "price":           o.price,
                    "delivery_type":   o.delivery_type,
                    "supply_id":       o.supply_id,
                    "warehouse_id":    o.warehouse_id,
                    "office_id":       o.office_id,
                    "cargo_type":      o.cargo_type,
                    "is_zero_order":   o.is_zero_order,
                    "skus":            o.skus,
                    "fetched_at":      o.fetched_at.isoformat() if o.fetched_at else None,
                }
                for o in items
            ],
            "total": total,
            "limit": limit,
            "offset": offset,
        }

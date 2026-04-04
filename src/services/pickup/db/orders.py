"""Сервис DB: Pickup — Чтение заказов самовывоза из БД."""
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.pickup.orders import PickupOrdersRepository
from src.services.base import BaseService


class PickupOrdersDbService(BaseService):

    async def get_orders(
        self,
        session: AsyncSession,
        date_from: str | None = None,
        date_to: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        repo = PickupOrdersRepository(session)
        total = await repo.count()
        items = await repo.get_filtered(
            date_from=date_from,
            date_to=date_to,
            limit=limit,
            offset=offset,
        )
        return {
            "data": [
                {
                    "order_id":               o.order_id,
                    "rid":                    o.rid,
                    "created_at":             o.created_at.isoformat() if o.created_at else None,
                    "article":                o.article,
                    "nm_id":                  o.nm_id,
                    "chrt_id":                o.chrt_id,
                    "price":                  o.price,
                    "converted_price":        o.converted_price,
                    "currency_code":          o.currency_code,
                    "converted_currency_code": o.converted_currency_code,
                    "final_price":            o.final_price,
                    "converted_final_price":  o.converted_final_price,
                    "cargo_type":             o.cargo_type,
                    "order_code":             o.order_code,
                    "pay_mode":               o.pay_mode,
                    "warehouse_id":           o.warehouse_id,
                    "warehouse_address":      o.warehouse_address,
                    "is_zero_order":          o.is_zero_order,
                    "skus":                   o.skus,
                    "fetched_at":             o.fetched_at.isoformat() if o.fetched_at else None,
                }
                for o in items
            ],
            "total": total,
            "limit": limit,
            "offset": offset,
        }

"""Репозиторий: Заказы Pickup (Click & Collect) — поля строго по api.Order schema из YAML."""
from datetime import datetime
from dateutil.parser import isoparse

from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.orders import PickupOrder

# 32767 // 21 cols = 1560 rows per batch
CHUNK_SIZE = 1560


def _parse_dt(val) -> datetime | None:
    if not val:
        return None
    try:
        return isoparse(str(val)).replace(tzinfo=None)
    except Exception:
        return None


class PickupOrdersRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    def _to_row(self, o: dict) -> dict:
        return {
            "order_id":               o.get("id") or o.get("order_id"),
            "rid":                    o.get("rid"),
            "created_at":             _parse_dt(o.get("createdAt") or o.get("created_at")),
            "article":                o.get("article"),
            "nm_id":                  o.get("nmId") or o.get("nm_id"),
            "chrt_id":                o.get("chrtId") or o.get("chrt_id"),
            "price":                  o.get("price"),
            "converted_price":        o.get("convertedPrice") or o.get("converted_price"),
            "currency_code":          o.get("currencyCode") or o.get("currency_code"),
            "converted_currency_code": o.get("convertedCurrencyCode") or o.get("converted_currency_code"),
            "final_price":            o.get("finalPrice") or o.get("final_price"),
            "converted_final_price":  o.get("convertedFinalPrice") or o.get("converted_final_price"),
            "cargo_type":             o.get("cargoType") or o.get("cargo_type"),
            "order_code":             o.get("orderCode") or o.get("order_code"),
            "pay_mode":               o.get("payMode") or o.get("pay_mode"),
            "warehouse_id":           o.get("warehouseId") or o.get("warehouse_id"),
            "warehouse_address":      o.get("warehouseAddress") or o.get("warehouse_address"),
            "is_zero_order":          bool(o.get("isZeroOrder") or o.get("is_zero_order", False)),
            "skus":                   o.get("skus"),
            "fetched_at":             datetime.utcnow(),
        }

    async def upsert_many(self, orders: list[dict]) -> int:
        if not orders:
            return 0
        rows = [self._to_row(o) for o in orders if o.get("id") or o.get("order_id")]
        if not rows:
            return 0

        update_cols = [k for k in rows[0] if k != "order_id"]

        for i in range(0, len(rows), CHUNK_SIZE):
            chunk = rows[i:i + CHUNK_SIZE]
            stmt = insert(PickupOrder).values(chunk)
            stmt = stmt.on_conflict_do_update(
                index_elements=["order_id"],
                set_={k: getattr(stmt.excluded, k) for k in update_cols},
            )
            await self._session.execute(stmt)
        await self._session.commit()
        return len(rows)

    async def count(self) -> int:
        result = await self._session.execute(select(func.count()).select_from(PickupOrder))
        return result.scalar_one()

    async def get_max_created_at(self) -> datetime | None:
        result = await self._session.execute(select(func.max(PickupOrder.created_at)))
        return result.scalar_one_or_none()

    async def get_filtered(
        self,
        date_from: str | None = None,
        date_to: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[PickupOrder]:
        query = select(PickupOrder)
        if date_from:
            query = query.where(PickupOrder.created_at >= date_from)
        if date_to:
            query = query.where(PickupOrder.created_at <= date_to)
        query = query.order_by(PickupOrder.created_at.desc()).limit(limit).offset(offset)
        result = await self._session.execute(query)
        return list(result.scalars().all())

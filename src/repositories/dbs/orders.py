"""Репозиторий: Заказы DBS — поля строго по WB API v3 OrderDBS schema."""
from datetime import datetime
from dateutil.parser import isoparse

from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.orders import DbsOrder

# 32767 // 30 cols = 1092 rows per batch
CHUNK_SIZE = 1092


def _parse_dt(val) -> datetime | None:
    if not val:
        return None
    try:
        return isoparse(str(val)).replace(tzinfo=None)
    except Exception:
        return None


class DbsOrdersRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    def _to_row(self, o: dict) -> dict:
        return {
            "order_id":               o.get("id") or o.get("order_id"),
            "order_uid":              o.get("orderUid") or o.get("order_uid"),
            "group_id":               o.get("groupId") or o.get("group_id"),
            "rid":                    o.get("rid"),
            "created_at":             _parse_dt(o.get("createdAt") or o.get("created_at")),
            "article":                o.get("article"),
            "color_code":             o.get("colorCode") or o.get("color_code"),
            "nm_id":                  o.get("nmId") or o.get("nm_id"),
            "chrt_id":                o.get("chrtId") or o.get("chrt_id"),
            "price":                  o.get("price"),
            "converted_price":        o.get("convertedPrice") or o.get("converted_price"),
            "currency_code":          o.get("currencyCode") or o.get("currency_code"),
            "converted_currency_code": o.get("convertedCurrencyCode") or o.get("converted_currency_code"),
            "final_price":            o.get("finalPrice") or o.get("final_price"),
            "converted_final_price":  o.get("convertedFinalPrice") or o.get("converted_final_price"),
            "scan_price":             o.get("scanPrice") or o.get("scan_price"),
            "wb_sticker_id":          o.get("wbStickerId") or o.get("wb_sticker_id"),
            "delivery_type":          o.get("deliveryType") or o.get("delivery_type"),
            "supply_id":              o.get("supplyId") or o.get("supply_id"),
            "warehouse_id":           o.get("warehouseId") or o.get("warehouse_id"),
            "office_id":              o.get("officeId") or o.get("office_id"),
            "cargo_type":             o.get("cargoType") or o.get("cargo_type"),
            "comment":                o.get("comment"),
            "is_zero_order":          bool(o.get("isZeroOrder") or o.get("is_zero_order", False)),
            "skus":                   o.get("skus"),
            "offices":                o.get("offices"),
            "address":                o.get("address"),
            "options":                o.get("options"),
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
            stmt = insert(DbsOrder).values(chunk)
            stmt = stmt.on_conflict_do_update(
                index_elements=["order_id"],
                set_={k: getattr(stmt.excluded, k) for k in update_cols},
            )
            await self._session.execute(stmt)
        await self._session.commit()
        return len(rows)

    async def count(self) -> int:
        result = await self._session.execute(select(func.count()).select_from(DbsOrder))
        return result.scalar_one()

    async def get_max_created_at(self) -> datetime | None:
        result = await self._session.execute(select(func.max(DbsOrder.created_at)))
        return result.scalar_one_or_none()

    async def get_filtered(
        self,
        date_from: str | None = None,
        date_to: str | None = None,
        delivery_type: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[DbsOrder]:
        query = select(DbsOrder)
        if date_from:
            query = query.where(DbsOrder.created_at >= date_from)
        if date_to:
            query = query.where(DbsOrder.created_at <= date_to)
        if delivery_type:
            query = query.where(DbsOrder.delivery_type == delivery_type)
        query = query.order_by(DbsOrder.created_at.desc()).limit(limit).offset(offset)
        result = await self._session.execute(query)
        return list(result.scalars().all())

"""Репозиторий: Сборочные задания FBS."""
from datetime import datetime

from dateutil.parser import isoparse
from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.orders import FbsOrder


def _parse_dt(val) -> datetime | None:
    if not val:
        return None
    if isinstance(val, datetime):
        return val.replace(tzinfo=None)
    try:
        dt = isoparse(str(val))
        return dt.replace(tzinfo=None)
    except (ValueError, TypeError):
        return None


# fbs_orders: 26 колонок → 32767 // 26 = 1260 строк/батч
CHUNK_SIZE = 1260


class FbsOrdersRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def upsert_many(self, orders: list[dict]) -> int:
        if not orders:
            return 0

        rows = []
        for o in orders:
            order_id = o.get("id") or o.get("order_id")
            if not order_id:
                continue
            rows.append({
                "order_id":              order_id,
                "order_uid":             o.get("orderUid") or o.get("order_uid"),
                "rid":                   o.get("rid"),
                "created_at":            _parse_dt(o.get("createdAt") or o.get("created_at")),
                "article":               o.get("article"),
                "color_code":            o.get("colorCode") or o.get("color_code"),
                "nm_id":                 o.get("nmId") or o.get("nm_id"),
                "chrt_id":               o.get("chrtId") or o.get("chrt_id"),
                "price":                 o.get("price"),
                "converted_price":       o.get("convertedPrice") or o.get("converted_price"),
                "currency_code":         o.get("currencyCode") or o.get("currency_code"),
                "converted_currency_code": o.get("convertedCurrencyCode") or o.get("converted_currency_code"),
                "delivery_type":         o.get("deliveryType") or o.get("delivery_type"),
                "supply_id":             o.get("supplyId") or o.get("supply_id"),
                "warehouse_id":          o.get("warehouseId") or o.get("warehouse_id"),
                "office_id":             o.get("officeId") or o.get("office_id"),
                "cargo_type":            o.get("cargoType") or o.get("cargo_type"),
                "cross_border_type":     o.get("crossBorderType") or o.get("cross_border_type"),
                "scan_price":            int(o.get("scanPrice") or 0) or None,
                "is_zero_order":         bool(o.get("isZeroOrder") or o.get("is_zero_order", False)),
                "comment":               o.get("comment"),
                "skus":                  o.get("skus"),
                "offices":               o.get("offices"),
                "address":               o.get("address"),
                "options":               o.get("options"),
                "fetched_at":            datetime.utcnow(),
            })

        if not rows:
            return 0

        total = 0
        for i in range(0, len(rows), CHUNK_SIZE):
            batch = rows[i:i + CHUNK_SIZE]
            stmt = insert(FbsOrder).values(batch)
            update_cols = {k: getattr(stmt.excluded, k) for k in batch[0] if k != "order_id"}
            stmt = stmt.on_conflict_do_update(index_elements=["order_id"], set_=update_cols)
            await self._session.execute(stmt)
            total += len(batch)

        await self._session.commit()
        return total

    async def count(self) -> int:
        result = await self._session.execute(select(func.count()).select_from(FbsOrder))
        return result.scalar_one()

    async def get_all(self, limit: int = 100, offset: int = 0) -> list[FbsOrder]:
        result = await self._session.execute(
            select(FbsOrder).order_by(FbsOrder.created_at.desc()).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def get_max_date(self) -> datetime | None:
        result = await self._session.execute(select(func.max(FbsOrder.created_at)))
        return result.scalar_one_or_none()

    async def get_filtered(
        self,
        date_from: str | None = None,
        date_to: str | None = None,
        delivery_type: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[FbsOrder]:
        query = select(FbsOrder)
        if date_from:
            query = query.where(FbsOrder.created_at >= _parse_dt(date_from))
        if date_to:
            query = query.where(FbsOrder.created_at <= _parse_dt(date_to))
        if delivery_type:
            query = query.where(FbsOrder.delivery_type == delivery_type)
        query = query.order_by(FbsOrder.created_at.desc()).limit(limit).offset(offset)
        result = await self._session.execute(query)
        return list(result.scalars().all())

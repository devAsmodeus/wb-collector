"""Репозиторий: Продажи и возвраты (отчёт WB)."""
from datetime import datetime

from dateutil.parser import isoparse
from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.reports import WbSaleReport


def _parse_dt(val) -> datetime | None:
    if not val:
        return None
    if isinstance(val, datetime):
        return val
    try:
        return isoparse(str(val))
    except (ValueError, TypeError):
        return None


class SaleReportsRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def upsert_many(self, items: list[dict]) -> int:
        if not items:
            return 0
        rows_map: dict[str, dict] = {}  # deduplicate by srid
        for item in items:
            srid = item.get("srid")
            if not srid:
                continue
            rows_map[srid] = {
                "srid": srid,
                "sale_id": item.get("saleID"),
                "date": _parse_dt(item.get("date")),
                "last_change_date": _parse_dt(item.get("lastChangeDate")),
                "supplier_article": item.get("supplierArticle"),
                "tech_size": item.get("techSize"),
                "barcode": item.get("barcode"),
                "total_price": item.get("totalPrice"),
                "discount_percent": item.get("discountPercent"),
                "is_supply": item.get("isSupply"),
                "is_realization": item.get("isRealization"),
                "warehouse_name": item.get("warehouseName"),
                "oblast": item.get("oblast"),
                "income_id": item.get("incomeID"),
                "odid": item.get("odid"),
                "nm_id": item.get("nmId"),
                "subject": item.get("subject"),
                "category": item.get("category"),
                "brand": item.get("brand"),
                "fetched_at": datetime.utcnow(),
            }
        rows = list(rows_map.values())
        if not rows:
            return 0
        # Batch upsert to avoid 32k parameter limit
        batch_size = max(1, 32000 // len(rows[0])) if rows else 1
        for i in range(0, len(rows), batch_size):
            batch = rows[i: i + batch_size]
            stmt = insert(WbSaleReport).values(batch)
            stmt = stmt.on_conflict_do_update(
                index_elements=["srid"],
                set_={
                    "sale_id": stmt.excluded.sale_id,
                    "date": stmt.excluded.date,
                    "last_change_date": stmt.excluded.last_change_date,
                    "supplier_article": stmt.excluded.supplier_article,
                    "tech_size": stmt.excluded.tech_size,
                    "barcode": stmt.excluded.barcode,
                    "total_price": stmt.excluded.total_price,
                    "discount_percent": stmt.excluded.discount_percent,
                    "is_supply": stmt.excluded.is_supply,
                    "is_realization": stmt.excluded.is_realization,
                    "warehouse_name": stmt.excluded.warehouse_name,
                    "oblast": stmt.excluded.oblast,
                    "income_id": stmt.excluded.income_id,
                    "odid": stmt.excluded.odid,
                    "nm_id": stmt.excluded.nm_id,
                    "subject": stmt.excluded.subject,
                    "category": stmt.excluded.category,
                    "brand": stmt.excluded.brand,
                    "fetched_at": stmt.excluded.fetched_at,
                },
            )
            await self._session.execute(stmt)
        await self._session.commit()
        return len(rows)

    async def get_max_date(self) -> datetime | None:
        """Возвращает максимальную дату last_change_date в БД (для инкрементального обновления)."""
        result = await self._session.execute(
            select(func.max(WbSaleReport.last_change_date))
        )
        return result.scalar_one_or_none()

    async def count(self) -> int:
        result = await self._session.execute(select(func.count()).select_from(WbSaleReport))
        return result.scalar_one()

    async def get_all(self, limit: int = 500, offset: int = 0) -> list[WbSaleReport]:
        result = await self._session.execute(
            select(WbSaleReport).order_by(WbSaleReport.date.desc()).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def get_filtered(self, date_from: str | None = None, date_to: str | None = None, limit: int = 500, offset: int = 0) -> list[WbSaleReport]:
        stmt = select(WbSaleReport)
        if date_from:
            stmt = stmt.where(WbSaleReport.date >= date_from)
        if date_to:
            stmt = stmt.where(WbSaleReport.date <= date_to)
        stmt = stmt.order_by(WbSaleReport.date.desc()).limit(limit).offset(offset)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

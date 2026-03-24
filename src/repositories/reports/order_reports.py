"""Репозиторий: Заказы (отчёт WB)."""
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.reports import WbOrderReport


class OrderReportsRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def upsert_many(self, items: list[dict]) -> int:
        if not items:
            return 0
        rows = [
            {
                "odid": item.get("odid"),
                "date": item.get("date"),
                "last_change_date": item.get("lastChangeDate"),
                "supplier_article": item.get("supplierArticle"),
                "tech_size": item.get("techSize"),
                "barcode": item.get("barcode"),
                "total_price": item.get("totalPrice"),
                "discount_percent": item.get("discountPercent"),
                "warehouse_name": item.get("warehouseName"),
                "oblast": item.get("oblast"),
                "income_id": item.get("incomeID"),
                "nm_id": item.get("nmId"),
                "subject": item.get("subject"),
                "category": item.get("category"),
                "brand": item.get("brand"),
                "is_cancel": item.get("isCancel"),
                "cancel_date": item.get("cancelDate"),
                "fetched_at": datetime.utcnow(),
            }
            for item in items
        ]
        stmt = insert(WbOrderReport).values(rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=["odid"],
            set_={
                "date": stmt.excluded.date,
                "last_change_date": stmt.excluded.last_change_date,
                "supplier_article": stmt.excluded.supplier_article,
                "tech_size": stmt.excluded.tech_size,
                "barcode": stmt.excluded.barcode,
                "total_price": stmt.excluded.total_price,
                "discount_percent": stmt.excluded.discount_percent,
                "warehouse_name": stmt.excluded.warehouse_name,
                "oblast": stmt.excluded.oblast,
                "income_id": stmt.excluded.income_id,
                "nm_id": stmt.excluded.nm_id,
                "subject": stmt.excluded.subject,
                "category": stmt.excluded.category,
                "brand": stmt.excluded.brand,
                "is_cancel": stmt.excluded.is_cancel,
                "cancel_date": stmt.excluded.cancel_date,
                "fetched_at": stmt.excluded.fetched_at,
            },
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return len(rows)

    async def get_all(self, limit: int = 500, offset: int = 0) -> list[WbOrderReport]:
        result = await self._session.execute(
            select(WbOrderReport).order_by(WbOrderReport.date.desc()).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def get_filtered(self, date_from: str | None = None, date_to: str | None = None, limit: int = 500, offset: int = 0) -> list[WbOrderReport]:
        stmt = select(WbOrderReport)
        if date_from:
            stmt = stmt.where(WbOrderReport.date >= date_from)
        if date_to:
            stmt = stmt.where(WbOrderReport.date <= date_to)
        stmt = stmt.order_by(WbOrderReport.date.desc()).limit(limit).offset(offset)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

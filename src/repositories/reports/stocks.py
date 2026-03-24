"""Репозиторий: Остатки на складах WB."""
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.reports import WbStock


class StocksRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def upsert_many(self, items: list[dict]) -> int:
        if not items:
            return 0
        rows = [
            {
                "last_change_date": item.get("lastChangeDate"),
                "supplier_article": item.get("supplierArticle"),
                "tech_size": item.get("techSize"),
                "barcode": item.get("barcode"),
                "quantity": item.get("quantity"),
                "is_supply": item.get("isSupply"),
                "is_realization": item.get("isRealization"),
                "quantity_full": item.get("quantityFull"),
                "in_way_to_client": item.get("inWayToClient"),
                "in_way_from_client": item.get("inWayFromClient"),
                "nm_id": item.get("nmId"),
                "subject": item.get("subject"),
                "category": item.get("category"),
                "brand": item.get("brand"),
                "sc_code": item.get("SCCode"),
                "price": item.get("Price"),
                "discount": item.get("Discount"),
                "warehouse_name": item.get("warehouseName"),
                "fetched_at": datetime.utcnow(),
            }
            for item in items
        ]
        # Stocks don't have a natural unique key — use bulk insert (truncate + insert strategy)
        # For simplicity, just insert all rows; caller can truncate if needed
        await self._session.execute(WbStock.__table__.insert(), rows)
        await self._session.commit()
        return len(rows)

    async def get_all(self, limit: int = 500, offset: int = 0) -> list[WbStock]:
        result = await self._session.execute(
            select(WbStock).order_by(WbStock.last_change_date.desc()).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def get_filtered(self, date_from: str | None = None, date_to: str | None = None, limit: int = 500, offset: int = 0) -> list[WbStock]:
        stmt = select(WbStock)
        if date_from:
            stmt = stmt.where(WbStock.fetched_at >= date_from)
        if date_to:
            stmt = stmt.where(WbStock.fetched_at <= date_to)
        stmt = stmt.order_by(WbStock.last_change_date.desc()).limit(limit).offset(offset)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

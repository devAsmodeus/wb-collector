"""Репозиторий: Заказы Самовывоз (Click & Collect)."""
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.orders import PickupOrder


class PickupOrdersRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def upsert_many(self, orders: list[dict]) -> int:
        """Вставляет или обновляет заказы Самовывоз. Возвращает кол-во обработанных записей."""
        if not orders:
            return 0
        rows = [
            {
                "order_id": o.get("id") or o.get("order_id"),
                "order_uid": o.get("orderUid") or o.get("order_uid"),
                "rid": o.get("rid"),
                "date": o.get("createdAt") or o.get("date"),
                "last_change_date": o.get("lastChangeDate") or o.get("last_change_date"),
                "warehouse_name": o.get("warehouseName") or o.get("warehouse_name"),
                "article": o.get("article"),
                "nm_id": o.get("nmId") or o.get("nm_id"),
                "subject": o.get("subject"),
                "category": o.get("category"),
                "brand": o.get("brand"),
                "name": o.get("name"),
                "tech_size": o.get("techSize") or o.get("tech_size"),
                "total_price": o.get("totalPrice") or o.get("total_price"),
                "discount_percent": o.get("discountPercent") or o.get("discount_percent"),
                "finished_price": o.get("finishedPrice") or o.get("finished_price"),
                "is_cancel": o.get("isCancel", False) or o.get("is_cancel", False),
                "cancel_date": o.get("cancelDate") or o.get("cancel_date"),
                "supplier_status": o.get("supplierStatus") or o.get("supplier_status"),
                "wb_status": o.get("wbStatus") or o.get("wb_status"),
                "fetched_at": datetime.utcnow(),
            }
            for o in orders
        ]
        stmt = insert(PickupOrder).values(rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=["order_id"],
            set_={
                "order_uid": stmt.excluded.order_uid,
                "rid": stmt.excluded.rid,
                "date": stmt.excluded.date,
                "last_change_date": stmt.excluded.last_change_date,
                "warehouse_name": stmt.excluded.warehouse_name,
                "article": stmt.excluded.article,
                "nm_id": stmt.excluded.nm_id,
                "subject": stmt.excluded.subject,
                "category": stmt.excluded.category,
                "brand": stmt.excluded.brand,
                "name": stmt.excluded.name,
                "tech_size": stmt.excluded.tech_size,
                "total_price": stmt.excluded.total_price,
                "discount_percent": stmt.excluded.discount_percent,
                "finished_price": stmt.excluded.finished_price,
                "is_cancel": stmt.excluded.is_cancel,
                "cancel_date": stmt.excluded.cancel_date,
                "supplier_status": stmt.excluded.supplier_status,
                "wb_status": stmt.excluded.wb_status,
                "fetched_at": stmt.excluded.fetched_at,
            },
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return len(rows)

    async def get_all(self, limit: int = 100, offset: int = 0) -> list[PickupOrder]:
        """Возвращает заказы Самовывоз из БД (последние сначала)."""
        result = await self._session.execute(
            select(PickupOrder).order_by(PickupOrder.date.desc()).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def get_filtered(
        self,
        date_from: str | None = None,
        date_to: str | None = None,
        status: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[PickupOrder]:
        """Возвращает заказы Самовывоз с фильтрацией."""
        query = select(PickupOrder)
        if date_from:
            query = query.where(PickupOrder.date >= date_from)
        if date_to:
            query = query.where(PickupOrder.date <= date_to)
        if status:
            query = query.where(PickupOrder.supplier_status == status)
        query = query.order_by(PickupOrder.date.desc()).limit(limit).offset(offset)
        result = await self._session.execute(query)
        return list(result.scalars().all())
